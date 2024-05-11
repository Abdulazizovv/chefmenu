from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
import json
from cart.cart import Cart
from main.models import Food
from table.models import Table
from users.models import Kitchen
from rest_framework.decorators import api_view
from rest_framework.response import Response

def cart(request, kitchen_id):
    table = None
    table_number = request.session.get('table_id' or None)
    cart = Cart(request)
    kitchen = get_object_or_404(Kitchen, id=int(kitchen_id))
    get_orders = False
    print(kitchen.get_orders)
    print(table_number)
    if table_number and kitchen.get_orders:
        get_orders = True
        table = get_object_or_404(Table, table_unique_id=table_number)
    context = {
        'cart': cart,
        'kitchen': kitchen,
        'table': table,
        'get_orders': get_orders,
    }
    return render(request, 'cart/cart.html', context=context)



@api_view(['POST'])
def add_cart(request):
    cart = Cart(request)
    response = {'status': 'error', 'cart': cart}  # Add 'cart' key to the response dictionary
    if request.method == 'POST':
        data = request.data
        product_id = data['product_id']
        kitchen_id = data['kitchen_id']
        # print(data)
        # print(kitchen_id)
        product = Food.objects.get(id=product_id)
        cart.add(product=product)
        response = {
            'status': 'success',
            'cart': cart,
            'total_price': cart.get_total_price(),  # Add 'total_price' key to the response dictionary
            'total_quantity': cart.get_total_quantity(),  # Add 'total_quantity' key to the response dictionary
        }
    return Response(response)

@api_view(['POST'])
def remove_cart(request):
    cart = Cart(request)
    response = {'status': 'error', 'cart': cart}  # Add 'cart' key to the response dictionary
    if request.method == 'POST':
        data = request.data
        product_id = data['product_id']
        kitchen_id = data['kitchen_id']
        product = Food.objects.get(id=product_id)
        cart.remove(product=product)
        response = {
            'status': 'success',
            'cart': cart,
            'total_price': cart.get_total_price(),  # Add 'total_price' key to the response dictionary
            'total_quantity': cart.get_total_quantity(),  # Add 'total_quantity' key to the response dictionary

        }
    return Response(response)


@api_view(['POST'])
def decrement_cart(request):
    cart = Cart(request)
    response = {'status': 'error', 'cart': cart}  # Add 'cart' key to the response dictionary
    if request.method == 'POST':
        data = request.data
        product_id = data['product_id']
        kitchen_id = data['kitchen_id']
        print(kitchen_id)
        product = Food.objects.get(id=product_id)
        cart.decrement(product=product)
        response = {
            'status': 'success',
            'cart': cart,
            'total_price': cart.get_total_price()  # Add 'total_price' key to the response dictionary
        }
    return Response(response)


@api_view(['POST'])
def clear_cart(request):
    cart = Cart(request)
    response = {'status': 'error', 'cart': cart}  # Add 'cart' key to the response dictionary
    if request.method == 'POST':
        data = request.data
        kitchen_id = data['kitchen_id']
        print(kitchen_id)
        cart.clear()
        response = {
            'status': 'success',
            'cart': cart,
            'total_price': cart.get_total_price()  # Add 'total_price' key to the response dictionary
        }
    return Response(response)


def cart_detail(request):
    return render(request, 'cart/cart_detail.html')


def checkout(request):
    return render(request, 'cart/checkout.html')


def order_create(request):
    return render(request, 'cart/order_create.html')

