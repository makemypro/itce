from rest_framework import views, response
from .serializers import SDPSerializer, IceCandidateSerializer, MessageSerializer, ChatMessageSerializer, AudioCallInitiationSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class SDPView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = SDPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room_id = kwargs['room_id']
        channel_name = f"chat_{room_id}"

        message = {
            'type': serializer.validated_data['type'],
            'jsep': serializer.validated_data['jsep'],
        }

        async_to_sync(get_channel_layer().group_send)(
            channel_name,
            {
                'type': 'chat.webrtc',
                'message': message,
            }
        )

        return response.Response(status=200)

class IceCandidateView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = IceCandidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room_id = kwargs['room_id']
        channel_name = f"chat_{room_id}"

        message = {
            'type': serializer.validated_data['type'],
            'candidate': serializer.validated_data['candidate'],
        }

        async_to_sync(get_channel_layer().group_send)(
            channel_name,
            {
                'type': 'chat.webrtc',
                'message': message,
            }
        )

        return response.Response(status=200)

class ChatMessageView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room_id = kwargs['room_id']
        channel_name = f"chat_{room_id}"

        message = {
            'type': 'chat.message',
            'message': serializer.validated_data['message'],
            'username': request.user.username,
        }

        async_to_sync(get_channel_layer().group_send)(
            channel_name,
            message
        )

        return response.Response(status=200)


class AudioCallInitiationView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = AudioCallInitiationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        caller_id = serializer.validated_data['caller_id']
        callee_id = serializer.validated_data['callee_id']

        room_id = f"{caller_id}_{callee_id}"
        channel_name = f"audio_call_{room_id}"

        async_to_sync(get_channel_layer().group_add)(
            channel_name,
            request.user.channel_name,
        )

        return response.Response(status=200)
