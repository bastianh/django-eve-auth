from urllib.parse import urlencode

from braces.views import AnonymousRequiredMixin
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.views.generic import RedirectView, TemplateView
from oauthlib.oauth2 import InsecureTransportError, MismatchingStateError
from requests import HTTPError
from requests_oauthlib import OAuth2Session

from .settings import CONFIG


def oauth_object(request, state=None):
    return OAuth2Session(CONFIG.get("CLIENT_ID"),
                         state=state,
                         scope=CONFIG.get("SCOPE", None),
                         redirect_uri=request.build_absolute_uri(reverse('eve_auth:callback')))


def query_reverse(viewname, kwargs=None, query_kwargs=None):
    """
    Custom reverse to add a query string after the url
    Example usage:
    url = my_reverse('my_test_url', kwargs={'pk': object.id}, query_kwargs={'next': reverse('home')})
    """
    url = reverse(viewname, kwargs=kwargs)

    if query_kwargs:
        return u'%s?%s' % (url, urlencode(query_kwargs))

    return url


class LoginView(AnonymousRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        authorization_url, state = oauth_object(self.request).authorization_url(CONFIG.get("AUTHORIZATION_BASE_URL"))
        self.request.session['eve_oauth_state'] = state
        return authorization_url


class CallbackView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):

        oauth = oauth_object(self.request, self.request.session.get('eve_oauth_state', '__missing_state'))
        login_failed_template = "%s:login_failed" % self.request.resolver_match.namespace
        try:
            del self.request.session['eve_oauth_state']
        except KeyError:
            pass

        try:
            token = oauth.fetch_token(CONFIG.get("TOKEN_URL"),
                                      client_secret=CONFIG.get("SECRET_KEY"),
                                      authorization_response=self.request.get_full_path())

            info = oauth.get(CONFIG.get("VERIFY_URL"))

            # TODO: add eve login to already authenticated login
            if not self.request.user.is_authenticated():
                eveuser = authenticate(eve_userdata=info.json(), token=token)
                if eveuser and eveuser.is_active:
                    login(self.request, eveuser)
                    return resolve_url(settings.LOGIN_REDIRECT_URL)
                return query_reverse(login_failed_template, query_kwargs={"msg": "auth failure: login failed"})

            return query_reverse(login_failed_template, query_kwargs={"msg": "auth failure: already logged in"})

        except HTTPError as e:
            return query_reverse(login_failed_template, query_kwargs={"msg": "auth failure: %s" % str(e)})

        except MismatchingStateError as e:
            return query_reverse(login_failed_template, query_kwargs={"msg": "auth failure: %s" % str(e)})

        except InsecureTransportError as e:
            return query_reverse(login_failed_template, query_kwargs={"msg": "auth failure: %r" % e})


class LoginFailedView(AnonymousRequiredMixin, TemplateView):
    template_name = 'eve_auth/login_failed.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['msg'] = self.request.GET.get("msg", "")
        return data


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(resolve_url(settings.LOGIN_REDIRECT_URL))
