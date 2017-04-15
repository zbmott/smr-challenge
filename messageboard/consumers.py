# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'


from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http


@channel_session_user_from_http
def ws_add(message):
    message.reply_channel.send({'accept': True})
    Group(message.content['path']).add(message.reply_channel)


@channel_session_user
def ws_disconnect(message):
    Group(message.content['path']).discard(message.reply_channel)
