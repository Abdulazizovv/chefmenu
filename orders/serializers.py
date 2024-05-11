from rest_framework import serializers
from .models import Orders, OrderItems
from main.models import Food

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class OrderItemsSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True)
    class Meta:
        model = OrderItems
        fields = ['food', 'quantity', 'price', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    foods = OrderItemsSerializer(many=True, read_only=True)
    class Meta:
        model = Orders
        fields = ['id', 'order_id', 'kitchen', 'user', 'foods', 'table', 'total_price', 'status', 'created', 'updated']