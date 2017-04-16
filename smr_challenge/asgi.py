# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

import os
from channels.asgi import get_channel_layer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smr_challenge.settings')

channel_layer = get_channel_layer()
