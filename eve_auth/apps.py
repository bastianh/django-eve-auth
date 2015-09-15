from __future__ import absolute_import, unicode_literals
import os

from django.apps import AppConfig

from . import settings as ea_settings


class EveAuthConfig(AppConfig):
    name = 'eve_auth'
    verbose_name = 'Django EvE App'

    def ready(self):
        if ea_settings.EVE_AUTH_ALLOW_INSECURE_TRANSPORT:
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        else:
            del os.environ["OAUTHLIB_INSECURE_TRANSPORT"]

