from django.urls import path
from .views import index, make_order, order_detail, get_orders, history_orders, change_order_status

app_name = 'orders'


urlpatterns = [
    path('', index, name='index'),
    path('make_order/', make_order, name='make_order'),
    path('order-detail/<int:order_id>/', order_detail, name='order_detail'),
    path('get-orders/<int:kitchen_id>/', get_orders, name='get_orders'),
    path('history-orders/', history_orders, name='history_orders'),
    path('change-order-status/', change_order_status, name='change_order_status'),
]
