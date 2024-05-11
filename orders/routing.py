from django.urls import re_path
from .consumers import OrderConsumer


websocket_urlpatterns = [
    re_path(r'ws/orders/(?P<kitchen_id>[^/]+)/$', OrderConsumer.as_asgi()),
]

