from django.contrib import admin

# Register your models here.

from messageboard.models import Channel, Topic, Like


class ChannelAdmin(admin.ModelAdmin):
    search_fields = ['name']

    list_display = ['name', 'created']

    list_filter = ['created']


class TopicAdmin(admin.ModelAdmin):
    search_fields = [
        'title',
        'channel__name',
        'created_by__username',
        'created_by__email'
    ]

    list_display = [
        'title',
        'channel',
        'created_by',
        'created'
    ]

    list_filter = ['created']

    raw_id_fields = ['created_by', 'channel']

    readonly_fields = ['path', 'depth', 'numchild']


class LikeAdmin(admin.ModelAdmin):
    search_fields = [
        'topic__title',
        'topic__channel__name',
        'user__username',
        'user__email'
    ]

    list_display = [
        'topic__title',
        'user',
        'created',
    ]

    list_filter = ['created']

    raw_id_fields = ['user', 'topic']

    def topic__title(self, obj):
        return obj.topic.title


admin.site.register(Channel, ChannelAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Like, LikeAdmin)
