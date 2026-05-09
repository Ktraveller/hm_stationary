import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        try:
            self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
            self.group_name = f"user_{self.user_id}"

            # join group
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )

            print(f"✅ User {self.user_id} connected to {self.group_name}")

            await self.accept()

        except Exception as e:
            print(f"❌ WebSocket connect error: {e}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
            print(f"❌ User {self.user_id} disconnected")

        except Exception as e:
            print(f"❌ WebSocket disconnect error: {e}")

    # -----------------------------
    # RECEIVE FROM DJANGO (group_send)
    # -----------------------------
    async def send_notification(self, event):
        try:
            message = event.get("message", "")

            await self.send(text_data=json.dumps({
                "type": "notification",
                "message": message
            }))

        except Exception as e:
            print(f"❌ Send notification error: {e}")