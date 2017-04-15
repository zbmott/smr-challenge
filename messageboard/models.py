# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.db import models

from treebeard.mp_tree import MP_Node


class Channel(models.Model):
    name = models.CharField(max_length=255)


class Topic(MP_Node):
    node_order_by = ['-created']

    channel = models.ForeignKey('messageboard.Channel')
    title = models.CharField(max_length=255)
    content = models.TextField()

    created_by = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    message = models.ForeignKey('messageboard.Topic')
    user = models.ForeignKey('auth.User')
