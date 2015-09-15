import evelink


class EVEApi(object):
    """ this class caches a connection to the eve api for workers
    """

    def __init__(self):
        self._api = evelink.api.API()

    def get_api(self):
        return self._api

    def get_eve_api(self):
        return evelink.eve.EVE(api=self.get_api())


eveapi = EVEApi()

