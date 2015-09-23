from __future__ import absolute_import, unicode_literals
import logging
import random
import string

from django.contrib.auth import get_user_model
from django.db import IntegrityError

from .models import EveLoginToken, Character

logger = logging.getLogger(__name__)


# noinspection PyMethodMayBeStatic
class EveSSOBackend(object):
    def authenticate(self, eve_userdata=None, token=None):
        character_id = eve_userdata.get('CharacterID')
        character_owner_hash = eve_userdata.get('CharacterOwnerHash')
        character_name = eve_userdata.get('CharacterName')
        logger.info("authenticate %r", character_name, extra={'token': token, "userdata": eve_userdata})
        logger.debug("test")
        logger.warn("test2")
        logger.critical("ICECREAM!")
        try:
            model = EveLoginToken.objects.get(character_id=character_id, character_owner_hash=character_owner_hash)
            return model.owner
        except EveLoginToken.DoesNotExist:
            # TODO check user generation allowed
            username = character_name
            character = Character.get_or_create(character_id, character_name)

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
            logintoken.token = token
            logintoken.character_owner_hash = character_owner_hash
            logintoken.save()

            return user

    def get_user(self, user_id):
        user = get_user_model()
        try:
            return user.objects.get(pk=user_id)
        except user.DoesNotExist:
            return None
