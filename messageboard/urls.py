# vim: ts=4:sw=4:expandtabs

__author__ = 'zmott@asmodeena.com'

from django.conf.urls import url, include

from rest_framework import routers

from messageboard import views
from messageboard.api.viewsets import TopicViewSet


router = routers.SimpleRouter()
router.register(r'topics', TopicViewSet)


urlpatterns = [
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
    url(r'^whoami/$', views.WhoAmI.as_view(), name='whoami'),
    url(r'^create-account/$', views.CreateAccount.as_view(), name='create-account'),
    url(r'^api/v1/', include(router.urls)),
]
