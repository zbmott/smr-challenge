# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

import bleach, re

from django.utils import timezone

from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from messageboard.models import Channel, Like, Topic

INVALID_CHANNEL_CHARS = re.compile(r'[^A-Za-z0-9_\-]')


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

    def validate_name(self, value):
        return INVALID_CHANNEL_CHARS.sub('', value)


class LikeSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=False)
    topic_id = serializers.IntegerField()

    class Meta:
        model = Like
        fields = ['user_id', 'topic_id']

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.pk
        like, _ = Like.objects.get_or_create(**validated_data)
        return like


class TopicSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer()
    key = serializers.IntegerField(source='pk', required=False)

    likes = serializers.SerializerMethodField(required=False)
    created_by = serializers.SerializerMethodField(required=False)
    parent = serializers.IntegerField(source='get_parent_pk', required=False)

    children = serializers.ListField(
        child=RecursiveField(),
        source='get_children_for_serializer',
        required=False
    )

    class Meta:
        model = Topic
        fields = [
            'pk', 'key', 'title', 'content',
            'channel', 'created_by', 'created',
            'likes', 'parent', 'children',
        ]
        read_only_fields = ['key']

    def create(self, validated_data):
        channel_serializer = ChannelSerializer(data=validated_data.pop('channel'))
        channel_serializer.is_valid()
        channel = channel_serializer.save()

        validated_data['created'] = timezone.now()
        validated_data['created_by'] = self.context['request'].user

        # This key in validated_data is weird because I used the
        # 'source' kwarg. 'get_parent_pk' was serialized as
        # 'parent', so now 'parent' is being deserialized into
        # 'get_parent_pk'.
        parent_pk = validated_data.pop('get_parent_pk', None)
        if parent_pk is None:
            topic = Topic.add_root(channel=channel, **validated_data)
        else:
            parent = Topic.objects.get(pk=parent_pk)
            topic = parent.add_child(channel=channel, **validated_data)

            # Because of the way MP_Node.add_child works, topic is
            # saved before it becomes the child of another node. The
            # The operation that moves it under its parent's tree doesn't
            # trigger the post_save handler, so I trigger it explicitly
            # here in order to preserve the real-time functionality.
            topic.save()

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

    def validate_content(self, value):
        return bleach.clean(value, tags=[], strip=True)

    def validate_title(self, value):
        # Could just assign validate_title = validate_content,
        # but this makes the stack trace more readable.
        return self.validate_content(value)
