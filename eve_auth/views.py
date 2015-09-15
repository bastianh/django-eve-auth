from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import resolve_url
from oauthlib.oauth2 import InsecureTransportError, MismatchingStateError
from requests import HTTPError
from requests_oauthlib import OAuth2Session

from .settings import CONFIG


def oauth_object(request, state=None):
    return OAuth2Session(CONFIG.get("CLIENT_ID"),
                         state=state,
                         redirect_uri=request.build_absolute_uri(reverse('eve_auth:callback')))


def login_view(request):
    oauth = oauth_object(request)
    authorization_url, state = oauth.authorization_url(CONFIG.get("AUTHORIZATION_BASE_URL"))

    request.session['eve_oauth_state'] = state

    return HttpResponseRedirect(authorization_url)


def callback_view(request):
    oauth = oauth_object(request, request.session.get('eve_oauth_state', '__missing_state'))
    try:
        del request.session['eve_oauth_state']
    except KeyError:
        pass

    try:
        token = oauth.fetch_token(CONFIG.get("TOKEN_URL"),
                                  client_secret=CONFIG.get("SECRET_KEY"),
                                  authorization_response=request.get_full_path())

        info = oauth.get(CONFIG.get("VERIFY_URL"))

        # TODO: add eve login to already authenticated login
        if not request.user.is_authenticated():
            eveuser = authenticate(eve_userdata=info.json())
            if eveuser and eveuser.is_active:
                login(request, eveuser)
                return HttpResponseRedirect(resolve_url(settings.LOGIN_REDIRECT_URL))
            return HttpResponse("auth failure: login failed")

        return HttpResponse("auth failure: already logged in")

    except HTTPError as e:
        return HttpResponse("auth failure: %s" % str(e))

    except MismatchingStateError as e:
        return HttpResponse("auth failure: %s" % str(e))

    except InsecureTransportError as e:
        return HttpResponse(e, status=500)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(resolve_url(settings.LOGIN_REDIRECT_URL))
