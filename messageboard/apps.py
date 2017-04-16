from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete


class MessageboardConfig(AppConfig):
    name = 'messageboard'

    def ready(self):
        # If users are ever allowed to edit their topics, using the
        # same handler for all of these signals means that we won't
        # have to write to code to push the updates to the clients.
        post_save.connect(model_changed_handler, sender=self.get_model('Channel'))
        post_save.connect(model_changed_handler, sender=self.get_model('Topic'))
        post_save.connect(model_changed_handler, sender=self.get_model('Like'))
        post_delete.connect(model_changed_handler, sender=self.get_model('Like'))


def model_changed_handler(sender, instance, **kw):
    instance.notify_group()
