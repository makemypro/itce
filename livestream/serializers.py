from rest_framework import serializers


class SDPSerializer(serializers.Serializer):
    type = serializers.CharField()
    jsep = serializers.JSONField()


class IceCandidateSerializer(serializers.Serializer):
    type = serializers.CharField()
    candidate = serializers.JSONField()


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class ChatMessageSerializer(serializers.Serializer):
    username = serializers.CharField()
    message = serializers.CharField()


class AudioCallInitiationSerializer(serializers.Serializer):
    caller_id = serializers.IntegerField()
    callee_id = serializers.IntegerField()
