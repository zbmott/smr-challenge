# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.utils import timezone

from rest_framework import serializers

from messageboard.models import Topic, Channel


class ChannelSerializer(serializers.ModelSerializer):
    key = serializers.IntegerField(source='pk', required=False)
    name = serializers.CharField()

    class Meta:
        model = Channel
        fields = ['key', 'name']
        read_only_fields = ['key']

    def create(self, validated_data):
        channel, _ = Channel.objects.get_or_create(**validated_data)
        return channel


class TopicSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer()
    key = serializers.IntegerField(source='pk', required=False)

    likes = serializers.SerializerMethodField(required=False)
    created_by = serializers.SerializerMethodField(required=False)
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = [
            'key', 'title', 'content',
            'channel', 'created_by',
            'created', 'likes', 'parent'
        ]
        read_only_fields = ['key']

    def create(self, validated_data):
        channel_serializer = ChannelSerializer(data=validated_data.pop('channel'))
        channel_serializer.is_valid()
        channel = channel_serializer.save()

        validated_data['created'] = timezone.now()
        validated_data['created_by'] = self.context['request'].user

        parent_pk = validated_data.pop('parent', None)
        if parent_pk is None:
            topic = Topic.add_root(channel=channel, **validated_data)
        else:
            parent = Topic.objects.get(pk=parent_pk)
            topic = parent.add_child(channel=channel, **validated_data)

        return topic

    def get_likes(self, obj):
        return obj.like_set.all().count()

    def get_created_by(self, obj):
        return obj.created_by.username

    def get_parent(self, obj):
        try:
            return obj.get_parent().pk
        except AttributeError:
            return None




