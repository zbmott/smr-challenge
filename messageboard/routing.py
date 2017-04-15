# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from channels.routing import route, include

websocket_routing = [
    route('websocket.connect', 'messageboard.consumers.ws_add'),
    route('websocket.disconnect', 'messageboard.consumers.ws_disconnect')
]
