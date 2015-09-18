from datetime import datetime
import json
import collections

import evelink
from django.core.cache import cache
from evelink.api import APIError
from requests import HTTPError


class DjangoCache(evelink.api.APICache):
    """An implementation of APICache using djangos cache framework

    it is using the default cache (make it configurable?)
    """

    def put(self, key, value, duration):
        cache.set("evelink_" + key, value, duration)

    def get(self, key):
        return cache.get("evelink_" + key)


APIResultEx = collections.namedtuple("APIResultEx", ["result", "timestamp", "expires", "apicallid"])


class API(evelink.api.API):
    """A wrapper around the EVE API."""

    def __init__(self, *args, **kwargs):
        self.api_key_object = None
        super().__init__(*args, **kwargs)

    def set_api_key_object(self, apikey_object):
        self.api_key_object = apikey_object
        if apikey_object:
            self.api_key = (apikey_object.key_id, apikey_object.vcode)
        else:
            self.api_key = None

    def get(self, path, params=None):
        """
        :rtype : APIResultEx
        """
        from eve_auth.models import ApiCall
        apicall = ApiCall(path=path, params=json.dumps(params), apikey=self.api_key_object)

        try:
            apiresult = super(API, self).get(path, params)
            if apiresult.timestamp:
                apicall.result_timestamp = datetime.utcfromtimestamp(apiresult.timestamp)
            if apiresult.expires:
                apicall.result_expires = datetime.utcfromtimestamp(apiresult.expires)
            apicall.success = True
            apicall.save()

            return APIResultEx(result=apiresult.result, expires=apiresult.expires,
                               timestamp=apiresult.timestamp, apicallid=apicall.pk)
        except APIError as apierror:
            apicall.api_error_code = apierror.code
            apicall.api_error_message = apierror.message
            apicall.save()
            # with db.engine.begin() as conn:
            #    keytable = ApiKey.__table__
            #    update = keytable.update().where(keytable.c.keyid == keyid)
            #    if keyid and int(apierror.code) in [222, 203]:
            #        update = update.values(error_count=99)
            #    else:
            #        update = update.values(error_count=keytable.c.error_count + 1)
            #    conn.execute(update)
            #    conn.execute(ApiCall.__table__.insert(), data)
            raise apierror
        except ConnectionError as e:
            apicall.http_error_code = e.errno
            if hasattr(e, "message"):
                apicall.http_error_message = str(e.message)
            else:
                apicall.http_error_message = str(e)
            apicall.save()
            # with db.engine.begin() as conn:
            #    conn.execute(ApiCall.__table__.insert(), data)
            raise e
        except HTTPError as e:
            apicall.http_error_code = e.errno
            if hasattr(e, "message"):
                apicall.http_error_message = str(e.message)
            else:
                apicall.http_error_message = str(e)
            apicall.save()
            # with db.engine.begin() as conn:
            #    conn.execute(ApiCall.__table__.insert(), data)
            raise e


class EVEApi(object):
    """ this class caches a connection to the eve api for workers
    """

    def __init__(self):
        self._api = API(cache=DjangoCache())

    def get_api(self, api_model=None) -> evelink.api.API:
        self._api.set_api_key_object(api_model)
        return self._api

    def get_eve_api(self) -> evelink.eve.EVE:
        return evelink.eve.EVE(api=self.get_api())

    def get_account_api(self, api_model) -> evelink.account.Account:
        return evelink.account.Account(api=self.get_api(api_model))


eveapi = EVEApi()
