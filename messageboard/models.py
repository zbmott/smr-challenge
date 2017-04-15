# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.db import models

from treebeard.mp_tree import MP_Node

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


class Channel(models.Model):
    name = models.CharField(max_length=255, unique=True)

    objects = JSONQuerySet.as_manager()

    def __unicode__(self):
        return self.name


class Topic(MP_Node):
    node_order_by = ['-created']

    channel = models.ForeignKey('messageboard.Channel')
    title = models.CharField(max_length=255)
    content = models.TextField()

    created_by = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)

    objects = JSONQuerySet.as_manager()

    class Meta:
        unique_together = ['title', 'channel']

    def __unicode__(self):
        return u"{title} ({channel})".format(title=self.title, channel=self.channel)


class Like(models.Model):
    message = models.ForeignKey('messageboard.Topic')
    user = models.ForeignKey('auth.User')
