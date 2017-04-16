from django.contrib import admin

# Register your models here.

from messageboard.models import Channel, Topic, Like

admin.site.register(Channel)
admin.site.register(Topic)
admin.site.register(Like)
