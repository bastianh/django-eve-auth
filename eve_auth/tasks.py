from __future__ import absolute_import
from datetime import datetime, timezone
import logging

from celery import shared_task
from celery.utils.log import get_task_logger

from .utils.eveapi import eveapi

logger2 = get_task_logger(__name__)
logger = logging.getLogger(__name__)


@shared_task
def check_key(key_id):
    from .models import ApiKey, Character, Corporation
    api_model = ApiKey.objects.get(pk=key_id)
    account = eveapi.get_account_api(api_model=api_model)
    info, _, _ = account.key_info()

    api_model.key_type = info.get("type")
    api_model.access_mask = info.get("access_mask")
    api_model.status = "active"
    expires = info.get("expire_ts")
    if expires:
        api_model.expires = datetime.utcfromtimestamp(expires).replace(tzinfo=timezone.utc)
    else:
        api_model.expires = None
    api_model.updated = datetime.now(timezone.utc)

    if api_model.key_type in ['account', 'char']:
        for charid, chardata in info.get("characters", {}).items():
            character = Character.get_or_create(character_id=charid, character_name=chardata.get('name'))
            api_model.characters.add(character)

    if api_model.key_type == "corp":
        corpinfo = list(info.get("characters").values())[0].get("corp")
        corp = Corporation.get_or_create(corporation_id=corpinfo.get("id"), corporation_name=corpinfo.get("name"))
        api_model.corporation = corp

    api_model.save()

    return 1


@shared_task
def update_character_info(character_id):
    from .models import Character, Corporation, Alliance
    eve = eveapi.get_eve_api()

    try:
        character = Character.objects.get(id=character_id)
    except Character.DoesNotExist:
        return False

    info, _, _ = eve.character_info_from_id(char_id=character_id)

    corp = info.get("corp", {})
    corpmodel = Corporation.get_or_create(corporation_id=corp.get("id"), corporation_name=corp.get("name"))
    character.corporation = corpmodel

    alliance_data = info.get("alliance", {})
    if corpmodel.alliance_id != alliance_data.get("id"):
        corpmodel.alliance = Alliance.get_or_create(alliance_id=alliance_data.get("id"),
                                                    alliance_name=alliance_data.get("name"))
        corpmodel.save()

    character.updated = datetime.utcnow().replace(tzinfo=timezone.utc)
    character.save()

    return True
