import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from users.models import Kitchen
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.serializers import serialize
from asgiref.sync import async_to_sync
from .models import Orders
from channels.layers import get_channel_layer

User = get_user_model()


@receiver(post_save, sender=Orders)
async def send_new_order_to_frontend(sender, instance, created, **kwargs):
    if created:
        print('New order created')
        new_order_data = {
            'id': instance.id,
            'status': instance.status,
            'created': instance.created.strftime('%Y-%m-%d %H:%M:%S'),
            'foods': [{'name': item.food.name, 'quantity': item.quantity} for item in instance.foods.all()]
        }
        channel_layer = get_channel_layer()
        try:
            await async_to_sync(channel_layer.group_send)(
                f'kitchen_orders_{instance.kitchen.kitchen_id}',
                {
                    'type': 'send_new_order',
                    'data': json.dumps(new_order_data)
                }
            )
        except Exception as e:
            print(f"Error sending new order to frontend: {e}")


class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.kitchen_id = self.scope['url_route']['kwargs']['kitchen_id']
        self.user = await self.get_user()
        if self.user.is_authenticated and self.user.is_kitchen:
            print(f'Kitchen {self.kitchen_id} connected')
            await self.channel_layer.group_add(
                f'kitchen_orders_{self.kitchen_id}',
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def send_new_order(self, event):
        print('Sending new order to frontend')
        await self.send(text_data=event['data'])

    async def disconnect(self, close_code):
        print("Disconnected")
        await self.channel_layer.group_discard(
            f'kitchen_orders_{self.kitchen_id}',
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle receiving data (e.g., order status updates)
        pass

    async def order_status_update(self, event):
        # Handle sending order status updates
        pass

    @database_sync_to_async
    def get_user(self):
        return self.scope['user']
