# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

import json

from channels import Group
from channels.auth import (
    channel_session,
    channel_session_user,
    channel_session_user_from_http
)


@channel_session
def topic_add(message, topic):
    message.reply_channel.send({'accept': True})
    message.reply_channel.send({
        'text': json.dumps({
            'topicList': [
                {'title': 'Test Topic 1'},
                {'title': 'Test Topic 2'},
                {'title': 'Test Topic 3'},
            ]
        })
    })
    message.channel_session['topic'] = topic
    Group(topic).add(message.reply_channel)


@channel_session
def topic_disconnect(message):
    Group(message.channel_session['topic']).discard(message.reply_channel)


def channel_list_add(message):
    message.reply_channel.send({'accept': True})
    message.reply_channel.send({
        'text': json.dumps({
            'channelList': [
                {'name': '/'},
                {'name': '/puppies'},
                {'name': '/kittens'}
            ]
        })
    })
    Group('channel-list').add(message.reply_channel)


def channel_list_disconnect(message):
    Group('channel-list').discard(message.reply_channel)
