# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'


from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import SessionAuthentication

from .serializers import TopicSerializer
from messageboard.models import Topic


class SessionAuthenticationSansCSRF(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class TopicViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()

    authentication_classes = [SessionAuthenticationSansCSRF]

    def create(self, request, *pos, **kw):
        if not request.user.is_authenticated():
            return Response(status=403)

        return super(TopicViewSet, self).create(request, *pos, **kw)

    def get_success_headers(self, data):
        return {}
