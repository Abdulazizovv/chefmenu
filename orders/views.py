from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import serializers, viewsets

from table.models import Table
from .models import Orders, OrderItems
from .serializers import OrderSerializer
from menu.decorators import only_kitchen
from users.models import User, Kitchen
from .models import Food
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cart.cart import Cart
from django.contrib import messages


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer


def get_orders(request, kitchen_id):
    kitchen = get_object_or_404(Kitchen, id=kitchen_id)
    orders = Orders.objects.filter(kitchen=kitchen).order_by('-created')
    
    serializer = OrderSerializer(orders, many=True)
    return JsonResponse(serializer.data, safe=False)


@only_kitchen
def index(request):
    if request.method == "POST":
        table = request.POST.get('table')
        request.session['table_id'] = table
        request.session['kitchen_id'] = request.user.kitchen.id
        request.session['is_kitchen_admin'] = True
        return redirect('main:foods', slug=request.user.kitchen.slug)
    kitchen = request.user.kitchen
    tables = Table.objects.filter(kitchen=kitchen)
    orders = Orders.objects.filter(kitchen=kitchen, status__in=["in_progress", "new"]).order_by('-created')
    context = {
        'orders': orders,
        'tables': tables,
    }
    return render(request, 'kitchen/orders/main.html', context=context)


@only_kitchen
def change_order_status(request):
    if request.method == "POST":
        kitchen = request.user.kitchen
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')
        order = get_object_or_404(Orders, id=order_id, kitchen=kitchen)
        order.status = status
        order.save()
        return redirect("orders:index")
    return JsonResponse({'status': 'error'})


@only_kitchen
def history_orders(request):
    orders = Orders.objects.all().order_by('-created')
    tables = Table.objects.filter(kitchen=request.user.kitchen)
    selected_status = request.GET.get('status' or None)
    date = request.GET.get('date' or None)
    selected_table = request.GET.get('table' or None)
    from_price = request.GET.get('fromPrice' or None)
    to_price = request.GET.get('toPrice' or None)
    if from_price:
        orders = orders.filter(total_price__gte=int(from_price))
    if to_price:
        orders = orders.filter(total_price__lte=int(to_price))
    if selected_table:
        orders = orders.filter(table__id=selected_table)
    if date:
        orders = orders.filter(created__date=date)
    if selected_status:
        orders = orders.filter(status=selected_status)
    
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    context = {
        'orders': orders,
        'tables': tables,
        'selected_status': selected_status,
        'selected_table': selected_table,
    }
    return render(request, 'kitchen/orders/orders_history.html', context=context)


def check_food(items, kitchen_id):
    for item in items:
        food = get_object_or_404(Food, id=item['product_id'])
        if food.kitchen.id != int(kitchen_id):
            return False
        return True


def make_order(request):
    cart = Cart(request)
    table_id = request.session.get('table_id')

    if request.method == "POST":
        
        kitchen_id = request.POST.get('kitchen_id')
        if kitchen_id:
            kitchen = get_object_or_404(Kitchen, id=int(kitchen_id))
            if not cart:
                messages.error(request, 'Savatingiz bo\'sh')
                return redirect('cart:cart', kitchen_id=kitchen_id)
            if not check_food(cart, kitchen_id):
                messages.error(request, 'Iltimos savatingizni tekshiring! Buyurtma berish uchun hamma taomlar bitta oshxonaniki bo\'lishi kerak.')
                return redirect('cart:cart', kitchen_id=kitchen_id)
            if kitchen.get_orders:  # Assuming get_orders is a method of Kitchen
                if table_id:
                    table = get_object_or_404(Table, table_unique_id=table_id)
                    total_price = cart.get_total_price()
                    order_items = []

                    for item in cart:
                        order_item = OrderItems.objects.create(
                            food=get_object_or_404(Food, id=item['product_id']),
                            quantity=item['quantity'],
                            price=item['price'],
                            total_price=item['total_price']
                        )
                        order_items.append(order_item)

                    order = Orders.objects.create(
                        kitchen=kitchen,
                        table=table,
                        total_price=total_price
                    )
                    order.foods.set(order_items)
                    order.save()
                    
                    cart.clear()
                    del request.session['table_id']  # Remove session variable
                    messages.success(request, 'Buyurtma qabul qilindi')
                    
                    # Redirect to a different URL after processing the POST request
                    return redirect('orders:order_detail', order_id=order.order_number)
                else:
                    messages.error(request, 'Stol tanlanmagan yoki bu oshxona buyurtmalarni qabul qilmayabdi!')
                    return redirect('main:menu', slug=kitchen.slug)
            else:
                messages.error(request, 'Xodimlar buyurtmalar qabul qila olmaydi!')
        else:
            messages.error(request, 'Xodimlar tanlanmagan!')
            return redirect('orders:order_detail', kitchen_id=kitchen_id)

    else:
        messages.error(request, 'Get method is not allowed')
        return redirect('main:index')


def order_detail(request, order_id):
    order = get_object_or_404(Orders, order_number=order_id)
    context = {
        'order': order,
    }
    return render(request, 'kitchen/orders/order_detail.html', context=context)