import evelink
from django.core.cache import cache


class DjangoCache(evelink.api.APICache):
    """An implementation of APICache using djangos cache framework

    it is using the default cache (make it configurable?)
    """

    def put(self, key, value, duration):
        cache.set("evelink_" + key, value, duration)

    def get(self, key):
        return cache.get("evelink_" + key)


class EVEApi(object):
    """ this class caches a connection to the eve api for workers
    """

    def __init__(self):
        self._api = evelink.api.API(cache=DjangoCache())

    def get_api(self, api_model=None) -> evelink.api.API:
        if api_model:
            self._api.api_key = (api_model.key_id, api_model.vcode)
        else:
            self._api.api_key = None
        return self._api

    def get_eve_api(self) -> evelink.eve.EVE:
        return evelink.eve.EVE(api=self.get_api())

    def get_account_api(self, api_model) -> evelink.account.Account:
        return evelink.account.Account(api=self.get_api(api_model))


eveapi = EVEApi()
