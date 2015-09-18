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
    from .models import EveApiKey, EveCharacter, EveCorporation
    api_model = EveApiKey.objects.get(pk=key_id)
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
            character, _ = EveCharacter.objects.get_or_create(character_id=charid, character_name=chardata.get('name'))
            api_model.characters.add(character)

    if api_model.key_type == "corp":
        corpinfo = list(info.get("characters").values())[0].get("corp")
        corp, _ = EveCorporation.objects.get_or_create(corporation_id=corpinfo.get("id"),
                                                       corporation_name=corpinfo.get("name"))
        api_model.corporation = corp

    api_model.save()

    return 1


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
