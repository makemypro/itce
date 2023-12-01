import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_name = f"chat_{room_id}"

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_id = self.scope["user"].id

        if data.get('sdp') or data.get('candidate'):
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'chat.webrtc',
                    'message': data,
                }
            )
        else:
            message = {
                'type': 'chat.message',
                'message': data['message'],
                'username': self.scope["user"].username,
            }

            await self.channel_layer.group_send(
                self.room_name,
                message
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'username': event.get('username', ''),
            'message': event.get('message', ''),
        }))

    async def chat_webrtc(self, event):
        await self.send(text_data=json.dumps({
            'type': event['message']['type'],
            'jsep': event['message'].get('jsep'),
            'candidate': event['message'].get('candidate'),
        }))
