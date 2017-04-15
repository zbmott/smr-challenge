# vim: ts=4:sw=4:expandtabs

__author__ = 'zmott@asmodeena.com'

from django.conf.urls import url

from messageboard import views


urlpatterns = [
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
    url(r'^whoami/$', views.WhoAmI.as_view(), name='whoami'),
    url(r'^create-account/$', views.CreateAccount.as_view(), name='create-account')
]
