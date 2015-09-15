from __future__ import absolute_import
from datetime import datetime

from celery import shared_task

from .utils.eveapi import eveapi


@shared_task
def update_character_info(character_id):
    from .models import EveCharacter, EveCorporation
    eve = eveapi.get_eve_api()

    try:
        character = EveCharacter.objects.get(character_id=character_id)
    except EveCharacter.DoesNotExist:
        return False

    info, _, _ = eve.character_info_from_id(char_id=character_id)

    corp = info.get("corp", {})
    corpmodel, _ = EveCorporation.objects.get_or_create(corporation_id=corp.get("id"),
                                                        defaults={"corporation_name": corp.get("name")})
    character.corporation = corpmodel

    alliance = info.get("alliance", {})
    if corpmodel.alliance_id != alliance.get("id"):
        corpmodel.alliance_id = alliance.get("id")
        corpmodel.alliance_name = alliance.get("name")
        corpmodel.save()

    character.updated = datetime.utcnow()
    character.save()

    return True
