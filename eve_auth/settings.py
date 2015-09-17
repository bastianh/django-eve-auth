from __future__ import absolute_import, unicode_literals
from importlib import import_module

from django.conf import settings

CONFIG_DEFAULTS = {
    "CLIENT_ID": None,
    "SECRET_KEY": None,
    "AUTHORIZATION_BASE_URL": "https://login.eveonline.com/oauth/authorize",
    "TOKEN_URL": "https://login.eveonline.com/oauth/token",
    "VERIFY_URL": "https://login.eveonline.com/oauth/verify",
}

EVE_AUTH_CONFIG = getattr(settings, 'EVE_AUTH_CONFIG', {})

CONFIG = CONFIG_DEFAULTS.copy()
CONFIG.update(EVE_AUTH_CONFIG)

EVE_AUTH_ALLOW_INSECURE_TRANSPORT = getattr(settings, "EVE_AUTH_ALLOW_INSECURE_TRANSPORT", settings.DEBUG)
