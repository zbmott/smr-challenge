from __future__ import unicode_literals

import json

from django.conf import settings
from django.apps import AppConfig
from django.db.models.signals import post_save

from channels import Group

class MessageboardConfig(AppConfig):
    name = 'messageboard'

    def ready(self):
        print "connecting handlers"
        post_save.connect(new_channel_handler, sender=self.get_model('Channel'))
        post_save.connect(new_topic_handler, sender=self.get_model('Topic'))


def new_channel_handler(sender, instance, created, **kw):
    if created:
        Group('channel-list').send({
            'text': json.dumps({
                'channelList': instance.__class__.objects.all().to_dict()
            })
        })


def new_topic_handler(sender, instance, created, **kw):
    if created:
        Group(instance.channel.name).send({
            'text': json.dumps({
                'topicList': instance.__class__.objects.filter(
                    channel__name=instance.channel.name
                ).to_dict()
            })
        })
        Group(settings.ROOT_CHANNEL_NAME).send({
            'text': json.dumps({
                'topicList': instance.__class__.objects.all()[:settings.ROOT_CHANNEL_LIMIT].to_dict()
            })
        })
