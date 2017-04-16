# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'


from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import SessionAuthentication

from .serializers import LikeSerializer, TopicSerializer
from messageboard.models import Like, Topic


class SessionAuthenticationSansCSRF(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class MessageBoardViewSet(GenericViewSet):
    authentication_classes = [SessionAuthenticationSansCSRF]

    def dispatch(self, request, *pos, **kw):
        if not request.user.is_authenticated():
            return Response(status=403)
        return super(MessageBoardViewSet, self).dispatch(request, *pos, **kw)


class TopicViewSet(CreateModelMixin, MessageBoardViewSet):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()


class LikeViewSet(CreateModelMixin, DestroyModelMixin, MessageBoardViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    lookup_field = 'topic_id'

    def filter_queryset(self, queryset):
        return queryset.filter(user_id=self.request.user.pk)
