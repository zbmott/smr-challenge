# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from rest_framework import serializers

from messageboard.models import Topic, Channel


class ChannelSerializer(serializers.ModelSerializer):
    key = serializers.IntegerField(source='pk')

    class Meta:
        model = Channel
        fields = ['key', 'name']
        read_only_fields = ['key']


class TopicSerializer(serializers.ModelSerializer):
    key = serializers.IntegerField(source='pk')
    channel = ChannelSerializer()

    class Meta:
        model = Topic
        fields = ['key', 'title', 'content', 'channel', 'created_by', 'created']
        read_only_fields = ['key']
