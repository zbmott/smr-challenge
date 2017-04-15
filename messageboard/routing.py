# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from channels.routing import route, include

topic_routing = [
    route('websocket.connect', 'messageboard.consumers.topic_add', path=r'(?P<topic>[a-zA-Z0-9_/]+)/$'),
    route('websocket.disconnect', 'messageboard.consumers.topic_disconnect')
]

channel_list_routing = [
    route('websocket.connect', 'messageboard.consumers.channel_list_add'),
    route('websocket.disconnect', 'messageboard.consumers.channel_list_disconnect')
]


routing = [
    include(topic_routing, path=r'^/topic'),
    include(channel_list_routing, path=r'^/_channellist')
]