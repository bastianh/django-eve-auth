from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^failed/$', views.LoginFailedView.as_view(), name='login_failed'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^callback/$', views.CallbackView.as_view(), name='callback'),
]
