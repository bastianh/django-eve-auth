from __future__ import absolute_import, unicode_literals

import random
import string
import celery.exceptions

from django.contrib.auth import get_user_model

from django.db import IntegrityError

from .models import EveLoginToken, EveCharacter
from .tasks import update_character_info
from . import settings as ea_settings


# noinspection PyMethodMayBeStatic
class EveSSOBackend(object):
    def authenticate(self, eve_userdata=None):
        character_id = eve_userdata.get('CharacterID')
        character_owner_hash = eve_userdata.get('CharacterOwnerHash')
        character_name = eve_userdata.get('CharacterName')

        try:
            model = EveLoginToken.objects.get(character_id=character_id, character_owner_hash=character_owner_hash)
            return model.owner
        except EveLoginToken.DoesNotExist:
            # TODO check user generation allowed
            username = character_name
            character, _ = EveCharacter.objects.get_or_create(character_id=character_id, character_name=character_name)

            user = None
            for i in range(0, 10):
                try:
                    user = get_user_model().objects.create_user(username=username)
                except IntegrityError:
                    username += random.choice(string.digits)
                    continue
                break

            if not user:
                return

            logintoken = EveLoginToken(owner=user)
            logintoken.character = character
            logintoken.character_owner_hash = character_owner_hash
            logintoken.save()

            result = update_character_info.apply_async([character_id])
            timeout = ea_settings.EVE_AUTH_UPDATE_CHARACTERINFO_TIMEOUT
            if timeout:
                try:
                    updated = result.get(timeout=timeout)
                    if updated:
                        character.refresh_from_db()
                except celery.exceptions.TimeoutError:
                    pass

            return user

    def get_user(self, user_id):
        user = get_user_model()
        try:
            return user.objects.get(pk=user_id)
        except user.DoesNotExist:
            return None
