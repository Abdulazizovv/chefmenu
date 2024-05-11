# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Orders
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from django.core.serializers import serialize



# @receiver(post_save, sender=Orders)
# def notify_new_order(sender, instance, created, **kwargs):
#     if created:
#         print(f"sender: {sender}")
#         channel_layer = get_channel_layer()
#         print(instance.kitchen.kitchen_id)
#         async_to_sync(channel_layer.group_send)(
#             f'kitchen_orders_{instance.kitchen.kitchen_id}',
#             {
#                 'type': 'send_latest_orders',
#                 'orders': serialize('json', [instance])
#             }
#         )