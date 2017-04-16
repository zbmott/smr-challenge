# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

import json

from django.db import models
from django.conf import settings

from channels import Group

from treebeard.mp_tree import MP_Node, MP_NodeQuerySet, get_result_class

from rest_framework.renderers import JSONRenderer


class JSONQuerySet(models.QuerySet):
    def _infer_serializer_class(self):
        """
        Try to infer a serializer class based on the model name.
        We can't import them directly into this file because that
        creates a dependency loop. 
        """
        import importlib

        serializer_name = "{name}Serializer".format(name=self.model.__name__)

        try:
            module = importlib.import_module('messageboard.api.serializers')
        except ImportError:
            return None

        try:
            serializer_class = getattr(module, serializer_name)
        except AttributeError:
            return None

        return serializer_class

    def to_dict(self, serializer_class=None):
        if serializer_class is None:
            serializer_class = self._infer_serializer_class()

        # If it's still None, this method is being invoked improperly.
        if serializer_class is None:
            msg = (u'You must either pass a serializer_class '
                   u'to this method or define ModelNameSerializer '
                   u'in messageboard.api.serializers.')
            raise ValueError(msg)

        serializer = serializer_class(self, many=True)
        return serializer.data

    def to_json(self, serializer_class=None):
        return JSONRenderer().render(self.to_dict(serializer_class=serializer_class))


class NotifyGroupMixin(object):
    group_name = NotImplemented
    notify_property_name = NotImplemented

    def get_group_name(self):
        return self.group_name

    def notify_group(self):
        group_name = self.get_group_name()
        queryset = self.get_notify_queryset(group_name)
        Group(group_name).send({
            'text': json.dumps({
                # In most cases, models that include this mixin will
                # also need to use JSONQuerySet. However, this is not
                # always the case, as in the Like model below.
                self.notify_property_name: queryset.to_dict()
            })
        })

    def get_notify_queryset(self, group_name):
        return self.__class__.objects.all()


class Channel(NotifyGroupMixin, models.Model):
    group_name = 'channel-list'
    notify_property_name = 'channelList'

    name = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = JSONQuerySet.as_manager()

    def __unicode__(self):
        return self.name


class TopicQuerySet(JSONQuerySet, MP_NodeQuerySet):
    pass


class Topic(NotifyGroupMixin, MP_Node):
    # Determines the number of nodes at any given level of the tree,
    # but decreases the maximum depth. A steplen of 5 allows more than
    # 60M children per node. The default is 4, which allows ~1.5M children.
    steplen = 5
    notify_property_name = 'topicList'

    channel = models.ForeignKey('messageboard.Channel')
    title = models.CharField(max_length=255)
    content = models.TextField()

    created_by = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)

    objects = TopicQuerySet.as_manager()

    class Meta:
        unique_together = ['title', 'channel']
        ordering = ['-created']

    def __unicode__(self):
        return u"{title} ({channel})".format(title=self.title, channel=self.channel)

    @classmethod
    def get_root_nodes(cls):
        # Explicitly set the ordering to 'path' so that treebeard
        # can correctly determine the last root to be added to the
        # tree. This is important when adding root nodes, because
        # treebeard determines the new root node's path by incrementing
        # the most recently-added root node's path. If this ordering
        # is inverted, treebeard will fail to add root nodes beyond the
        # second one.
        # TODO: Report (and fix) this issue in django-treebeard.
        return get_result_class(cls).objects.filter(depth=1).order_by('path')

    def get_group_name(self):
        return self.channel.name

    def notify_group(self):
        super(Topic, self).notify_group()
        queryset = self.__class__.objects.all()[:settings.ROOT_CHANNEL_LIMIT]
        Group(settings.ROOT_CHANNEL_NAME).send({
            'text': json.dumps({
                'topicList': queryset.to_dict()
            })
        })

    def get_notify_queryset(self, group_name):
        return self.__class__.objects.filter(channel__name=group_name)


class Like(NotifyGroupMixin, models.Model):
    topic = models.ForeignKey('messageboard.Topic')
    user = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"{user} => {topic}".format(
            user=self.user.username,
            topic=self.topic.title
        )

    def notify_group(self):
        self.topic.notify_group()
