import json
from django.shortcuts import get_object_or_404, redirect, render
import random
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate, logout
from table.models import Table
from users.models import User, Kitchen
from .models import ContactMessages, Menu, FoodCategory, Food
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from menu.decorators import only_kitchen
from cart.cart import Cart
from orders.models import Orders
from verification.utils import check_verification_code
from reviews.models import ReviewKitchen, ReviewFood
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
import datetime




def generate_kitchen_stats(kitchen):
    reviews = ReviewKitchen.objects.filter(kitchen=kitchen)
    total_reviews = reviews.count()
    total_foods = Food.objects.filter(kitchen=kitchen, is_active=True).count()

    # Calculate the date at the beginning of the current year
    current_year = timezone.now().year
    start_of_year = timezone.make_aware(datetime.datetime(current_year, 1, 1))

    # Get the total sum of orders for each month from the start of the year
    monthly_order_stats = (
        Orders.objects
        .filter(kitchen=kitchen, created__gte=start_of_year)
        .annotate(month=TruncMonth('created'))
        .values('month')
        .annotate(total_sum=Sum('total_price'), total_orders=Count('id'))
        .order_by('month')
    )

    # Get the total sum and count of today's orders
    today = timezone.now().date()
    today_order_stats = (
        Orders.objects
        .filter(kitchen=kitchen, created__date=today)
        .aggregate(total_sum=Sum('total_price'), total_orders=Count('id'))
    )

    # Get the total sum and count of this month's orders
    this_month = timezone.now().month
    this_month_order_stats = (
        Orders.objects
        .filter(kitchen=kitchen, created__month=this_month)
        .aggregate(total_sum=Sum('total_price'), total_orders=Count('id'))
    )
    most_sold_foods = Food.objects.filter(orderitems__orders__kitchen=kitchen).annotate(sold_quantity=Sum('orderitems__quantity')).order_by('-sold_quantity')[:3]

    stats = {
        "monthly_order_dates": [item['month'].strftime('%B') for item in monthly_order_stats],
        "monthly_order_sums": [item['total_sum'] for item in monthly_order_stats],
        "monthly_order_counts": [item['total_orders'] for item in monthly_order_stats],
        "most_sold_food_names": [item.name for item in most_sold_foods],
        "most_sold_food_quantities": [item.sold_quantity for item in most_sold_foods],
    }

    stats = json.dumps(stats)
    
    # most_sold_foods = json.dumps(list(most_sold_foods.values('name', 'sold_quantity')))
    return {
        'total_reviews': total_reviews,
        'today_order_stats': today_order_stats,
        'this_month_order_stats': this_month_order_stats,
        'total_foods': total_foods,
        'monthly_order_stats': monthly_order_stats,
        "stats": stats,
        "most_sold_foods": most_sold_foods,
    }
    




def index(request):
    if request.user.is_authenticated:
        if request.user.is_kitchen:
            kitchen = request.user.kitchen
            stats = generate_kitchen_stats(kitchen)
            context = {
                'parent': 'kitchen',
                'child': 'dashboard',
                'kitchen': kitchen,
                'stats': stats,
            }
            return render(request, 'kitchen/index.html', context=context)
    page = request.GET.get('page', 1)
    all_kitchens = Kitchen.objects.all().order_by('created')
    paginator  = Paginator(all_kitchens, 6)
    try:
        kitchens = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        kitchens = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        kitchens = paginator.page(paginator.num_pages)
    context = {
        "kitchens": kitchens,
    }
    return render(request, 'main/index.html', context=context)


def about(request):
    return render(request, "main/about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')
        ContactMessages.objects.create(name=name, phone_number=phone_number, message=message)
        messages.success(request, 'Muvaffaqqiyatli yuborildi! Tez orada siz bilan bog\'lanamiz!')
        return redirect('main:contact')
    return render(request, "main/contact.html")



def register_kitchen(request):
    return render(request, 'kitchen/auth/register2.html')


@only_kitchen
def kitchen_user_profile(request):
    
    return render(request, "kitchen/user_profile.html")



@only_kitchen
def kitchen_profile(request):
    kitchen = request.user.kitchen
    phone_numbers = kitchen.phone_numbers.all()
    if request.method == 'POST':
        section = request.POST.get('section')
        if section == 'profile':
            name = request.POST.get('kitchenName')
            description = request.POST.get('kitchenInfo')
            image = request.FILES.get('kitchenImage')
            kitchen.title = name
            kitchen.info = description
            if image:
                kitchen.image = image
            kitchen.save()
            messages.success(request, 'Muvaffaqqiyatli saqlandi!')
            return redirect('main:kitchen_profile')
        elif section == 'contact':
            address = request.POST.get('kitchenAddress')
            phone_number = request.POST.getlist('kitchenPhoneNumber[]')
            phone_numbers.delete()
            for number in phone_number:
                kitchen.phone_numbers.create(number=number)
            kitchen.address = address
            kitchen.save()

            messages.success(request, 'Muvaffaqqiyatli saqlandi!')
            return redirect('main:kitchen_profile')
        elif section == 'social':
            telegram = request.POST.get('kitchenTelegram')
            instagram = request.POST.get('kitchenInstagram')
            facebook = request.POST.get('kitchenFacebook')
            twitter = request.POST.get('kitchenTwitter')
            kitchen.telegram = telegram
            kitchen.instagram = instagram
            kitchen.facebook = facebook
            kitchen.twitter = twitter
            kitchen.save()
            messages.success(request, 'Muvaffaqqiyatli saqlandi!')
            return redirect('main:kitchen_profile')

    context = {
        "kitchen": kitchen,
        "phone_numbers": phone_numbers,
    }
    return render(request, "kitchen/kitchen_profile.html", context=context)


def user_profile(request):
    user = request.user
    context = {
        "user": user,
    } 
    return render(request, "main/user_profile.html", context=context)


def kitchen_info(request, kitchen_slug):
    kitchen = get_object_or_404(Kitchen, slug=kitchen_slug)
    context = {
        "kitchen": kitchen,
    }
    return render(request, "main/kitchen_info.html", context=context)



def kitchen_detail(request, slug):
    table_id = request.session.get('table_id' or None)
    table = None
    if table_id:
        table = Table.objects.get(table_unique_id=table_id)
    kitchen = get_object_or_404(Kitchen, slug=slug)
    comments = ReviewKitchen.objects.filter(kitchen=kitchen).order_by("-created")
    categories = FoodCategory.objects.filter(kitchen=kitchen)
    context = {
        "kitchen": kitchen,
        "categories": categories,
        "table": table,
        "comments_count": comments.count(),
    }
    return render(request, "main/kitchen_categories.html", context=context)


def kitchen_foods(request, slug):
    kitchen = get_object_or_404(Kitchen, slug=slug)
    categories = FoodCategory.objects.filter(kitchen=kitchen)

    foods = Food.objects.filter(kitchen=kitchen)
    cart = Cart(request)
    context = {
        "kitchen": kitchen, 
        "categories": categories,
        "foods": foods,
        "cart": cart,
    }
    return render(request, "main/kitchen_foods.html", context=context)


def category_foods(request, kitchen_slug, category_slug):
    kitchen = get_object_or_404(Kitchen, slug=kitchen_slug)
    categories = FoodCategory.objects.filter(kitchen=kitchen)
    category = get_object_or_404(FoodCategory, slug=category_slug)
    foods = Food.objects.filter(category=category)
    context = {
        "categories": categories,
        "kitchen": kitchen,
        "category": category,
        "foods": foods
    }
    return render(request, "main/category_foods.html", context=context)


def redirect_menu(request, kitchen_id, table_id):
    kitchen = get_object_or_404(Kitchen, kitchen_id=kitchen_id)
    request.session['table_id'] = table_id
    request.session['kitchen_id'] = kitchen_id
    return redirect('main:menu', slug=kitchen.slug)


def check_phone_number_exists(number):
    try:
        User.objects.get(phone_number=number)
        return True
    except Exception as e:
        print(e)
        return False


def register(request):
    if request.user.is_authenticated:
        messages.warning(request=request, message='You are already authenticated')
        return redirect('main:index')
    if request.method == 'POST':
        print(request.POST)
        phone_number = request.POST.get('phone_number')
        name = request.POST.get('name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        verification_code = request.POST.get('verification_code')
        print(f"verify = {verification_code}")
        if check_verification_code(phone_number=phone_number, code=verification_code):
            if password1 == password2:
                try:
                    user = User.objects.create_user(
                        phone_number=phone_number,
                        password=password1,
                        full_name=name
                    )
                    user = authenticate(request, phone_number=phone_number, password=password1)
                    if user:
                        login(request, user)
                        messages.success(request, "Muvaffaqqiyatli ro'yxatdan o'tildi!")
                        return redirect('main:index')
                except:
                    messages.error(request, "Nimadir xato ketdi!")
                    return redirect('main:register')
            
            messages.error(request, "Parollar mos emas!")
    return render(request, 'kitchen/auth/register.html')


def login_(request):
    if request.user.is_authenticated:
        messages.warning(request=request, message='You are already authenticated')
        return redirect('main:index')
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        print(phone_number)
        user = authenticate(request, phone_number=phone_number, password=password)
        print(user)
        if user:
            login(request, user)
            return redirect('main:index')
        else:
            print('User not found')
            messages.warning(request=request, message='Telefon raqam yoki parol noto\'g\'ri')
            return redirect('main:login')
    return render(request, 'kitchen/auth/login.html')


def logout_(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('main:index')
    messages.warning(request=request, message="You are not authenticated")
    return redirect('main:index')
    