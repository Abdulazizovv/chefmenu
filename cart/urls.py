from django.urls import path
from .views import cart, add_cart, remove_cart, decrement_cart, clear_cart, cart_detail, checkout, order_create


app_name = 'cart'

urlpatterns = [
    path('add/', add_cart, name='add_cart'),
    path('<int:kitchen_id>/', cart, name='cart'),
    path('remove/', remove_cart, name='remove_cart'),
    path('decrement/', decrement_cart, name='decrement_cart'),
    path('clear/', clear_cart, name='clear_cart'),
    path('cart_detail/', cart_detail, name='cart_detail'),
    path('checkout/', checkout, name='checkout'),
    path('order_create/', order_create, name='order_create'),
    
]