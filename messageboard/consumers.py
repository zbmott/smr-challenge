# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

import json

from django.conf import settings

from channels import Group
from channels.auth import (
    channel_session,
    channel_session_user,
    channel_session_user_from_http
)

from messageboard.models import Channel, Topic


@channel_session
def topic_add(message, channel):
    message.reply_channel.send({'accept': True})

    # Normally, a users sees all the topics posted to
    # the channel they're currently connected to.
    topicList = Topic.objects.filter(channel__name=channel).to_dict()
    if channel == settings.ROOT_CHANNEL_NAME:
        # However, users who are connected to the root channel see
        # the 25 (by default) most recent topics posted to ALL channels.
        topicList = Topic.objects.all()[:settings.ROOT_CHANNEL_LIMIT]

    message.reply_channel.send({
        'text': json.dumps({
            'topicList': topicList
        })
    })
    message.channel_session['channel'] = channel
    Group(channel).add(message.reply_channel)


@channel_session
def topic_disconnect(message):
    Group(message.channel_session['channel']).discard(message.reply_channel)


def channel_list_add(message):
    message.reply_channel.send({'accept': True})
    message.reply_channel.send({
        'text': json.dumps({
            'channelList': Channel.objects.all().to_dict()
        })
    })
    Group('channel-list').add(message.reply_channel)


def channel_list_disconnect(message):
    Group('channel-list').discard(message.reply_channel)
