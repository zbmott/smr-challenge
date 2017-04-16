from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete


class MessageboardConfig(AppConfig):
    name = 'messageboard'

    def ready(self):
        print "connecting handlers"
        post_save.connect(post_save_handler, sender=self.get_model('Channel'))
        post_save.connect(post_save_handler, sender=self.get_model('Topic'))
        post_save.connect(post_save_handler, sender=self.get_model('Like'))
        post_delete.connect(post_delete_handler, sender=self.get_model('Like'))


def post_save_handler(sender, instance, created, **kw):
    if created:
        instance.notify_group()


def post_delete_handler(sender, instance, **kw):
    instance.notify_group()
