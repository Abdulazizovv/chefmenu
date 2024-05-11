import logging
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Food, FoodCategory, Menu, FoodVariant
from users.models import User
from django.contrib import messages
from main.forms import FoodVariantFormset
from .decorators import only_kitchen
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


@only_kitchen
def kitchen_menu(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name' or None)
        if category_name:
            user = get_object_or_404(User, id=request.user.id)
            kitchen = user.kitchen
            category = FoodCategory.objects.create(
                title=category_name,
                kitchen=kitchen
            )
            category.save()
        return redirect('menu:kitchen_menu')
    else:
        user = get_object_or_404(User, id=request.user.id)
        kitchen = user.kitchen
        categories = FoodCategory.objects.filter(kitchen=kitchen)
        menu = get_object_or_404(Menu, kitchen=kitchen)
        foods = menu.foods.values()
        category_counts = {}
        for category in categories:
            category_counts[category] = Food.objects.filter(category=category).count()
        context = {
            'menu': menu,
            'foods': foods,
            'categories': categories,
            'category_counts': category_counts,
            'parent': 'kitchen',
            'child': 'menu'
        }
        return render(request, 'kitchen/menu.html', context=context)


@only_kitchen
def all_foods(request):
    if request.method == 'GET':
        user = get_object_or_404(User, id=request.user.id)
        kitchen = user.kitchen
        categories = FoodCategory.objects.filter(kitchen=kitchen)
        foods = Food.objects.filter(kitchen=kitchen)
        context = {
            'foods': foods,
            'categories': categories,
        }
        return render(request, 'kitchen/all-foods.html', context=context)


@only_kitchen
def food_detail(request, id):
    if request.method == 'GET':
        user = get_object_or_404(User, id=request.user.id)
        kitchen = user.kitchen
        food = get_object_or_404(Food, id=id)
        context = {
            'food': food
        }
        return render(request, 'kitchen/food_detail.html', context=context)


@only_kitchen
def delete_category(request):
    if request.method == 'POST':
        print(request.POST)
        id = request.POST.get('category_id')
        category = get_object_or_404(FoodCategory, id=id)
        if category.kitchen == request.user.kitchen:
            messages.success(request, "Kategoriya o'chirildi!")
            category.delete()
            return redirect('menu:kitchen_menu')
        else:
            messages.error(request, "Sizga ruxsat yo'q!")
            return redirect('menu:kitchen_menu')
    messages.warning(request, "GET so'rovni qo'llab-quvvatlamaymiz!")
    return redirect('menu:kitchen_menu')


@only_kitchen
def edit_category(request):
    if request.method == 'POST':
        id = request.POST.get('category_id')
        title = request.POST.get('category_name')
        category = get_object_or_404(FoodCategory, id=id)
        if category.kitchen == request.user.kitchen:
            category.title = title
            category.save()
            messages.success(request, "Kategoriya o'zgartirildi!")
            return redirect('menu:kitchen_menu')
        else:
            messages.error(request, "Sizga ruxsat yo'q!")
            return redirect('menu:kitchen_menu')
    messages.warning(request, "GET so'rovni qo'llab-quvvatlamaymiz!")
    return redirect('menu:kitchen_menu')


@only_kitchen
def category_foods(request, title):
        category = get_object_or_404(FoodCategory, slug=title)
        foods = Food.objects.filter(category=category).order_by('name').prefetch_related('variants')
        context = {
            'category': category,
            'foods': foods
        }
        return render(request, 'kitchen/category_foods.html', context=context)



@only_kitchen
def edit_food(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    if request.method == 'POST':
        pass
    categories = FoodCategory.objects.filter(kitchen=request.user.kitchen)
    context = {
        "food": food,
        "categories": categories,
    }
    return render(request, "kitchen/edit-food.html", context=context)



@only_kitchen
def add_food(request):
    if request.method == 'POST':
        food_name = request.POST.get('foodName')
        food_category = request.POST.get('foodCategory')
        food_description = request.POST.get('foodDescription')
        food_price = request.POST.get('foodPrice')
        food_image = request.FILES.get('foodImage')
        redirect_url = request.POST.get('redirectUrl')
        has_variants = request.POST.get('hasVariants')
        variant_names = request.POST.getlist('variantNames[]')
        variant_descriptions = request.POST.getlist('variantDescriptions[]')
        variant_prices = request.POST.getlist('variantPrices[]')
        variant_images = request.FILES.getlist('variantImages[]')

        category = get_object_or_404(FoodCategory, id=food_category)

        # Validate food image
        if not food_image:
            messages.error(request, "Food image is required")
            return redirect('menu:category_foods', title=category.slug)
        validator = FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
        try:
            validator(food_image)
        except ValidationError as e:
            messages.error(request, "Invalid food image format. Only JPG, JPEG, and PNG are allowed.")
            return redirect('menu:category_foods', title=category.slug)
        
        # Save food data to the database
        food = Food.objects.create(
            kitchen=request.user.kitchen,
            category=category,
            name=food_name,
            description=food_description,
            price=food_price,
            image=food_image
        )

        # if redirect_url:
        #     return redirect(redirect_url, food.id)
        # print(redirect_url)

        # Save food variants if any
        if has_variants:
            for name, description, price, image in zip(variant_names, variant_descriptions, variant_prices, variant_images):
                FoodVariant.objects.create(
                    food=food,
                    name=name,
                    description=description,
                    price=price,
                    image=image
                )
            food.has_variants = True
            food.save()
        messages.success(request, "Taom qo'shildi!")
        return redirect('menu:category_foods', title=category.slug)
    else:
        food_variant_form_set = FoodVariantFormset()
        user = get_object_or_404(User, id=request.user.id)
        kitchen = user.kitchen
        categories = FoodCategory.objects.filter(kitchen=kitchen)
        context = {
            "user": user,
            "kitchen": kitchen,
            "categories": categories,
            "food_variant_formset": food_variant_form_set
        }
        return render(request, "kitchen/add_food.html", context=context)
    

@only_kitchen
def delete_food(request):
    print("working")
    if request.method == "POST":
        food_id = request.POST.get('foodId' or None)
        from_ = request.POST.get('from' or None)
        category_slug = request.POST.get('categorySlug' or None)
        if not food_id:
            return redirect("menu:kitchen_menu")
        food = get_object_or_404(Food, id=food_id)
        try:
            food.category = None
            food.save()
            messages.success(request, "Taom o'chirildi!")
        except Exception as err:
            logging.error(err)
            messages.error(request, "Nimadir xato...!")
        if from_ == "all-foods":
            return redirect("menu:all_foods")
        return redirect('menu:category_foods', category_slug)
    messages.error(request, "GET metod ruxsat berilmagan!")
    return redirect('menu:kitchen_menu')


@only_kitchen
def edit_food_details(request):
    if request.method == 'POST':
        print("working")
        food_id = request.POST.get('foodId')
        food_name = request.POST.get('foodName')
        food_category_id = request.POST.get('foodCategory')
        food_description = request.POST.get('foodDescription')
        food_price = request.POST.get('foodPrice')
        food_image = request.FILES.get('foodImage')
        print(food_category_id)
        # Validate food_id
        if not food_id:
            return HttpResponseBadRequest("Food ID is required")

        # Get food object
        food = get_object_or_404(Food, id=food_id)

        # Get category object
        category = get_object_or_404(FoodCategory, id=food_category_id)

        # Update food details
        food.name = food_name
        food.category = category
        food.description = food_description
        food.price = food_price

        # Update food image if provided
        if food_image:
            food.image = food_image

        # Save changes
        food.save()

        messages.success(request, "Food details updated successfully!")
        return redirect("menu:edit_food", food_id=food_id)

    # Invalid request method
    return HttpResponseBadRequest("Invalid request method")


def edit_food_variant(request, food_id):
    pass


@only_kitchen
def add_food_variant(request):
    food_id = request.POST.get('foodId')
    food = get_object_or_404(Food, id=food_id)
    if request.method == 'POST':
        name = request.POST.get('variantName')
        if not name:
            messages.error(request, "Taom turi nomi majburiy")
            return redirect('menu:edit_food', food_id=food_id)
        description = request.POST.get('variantDescription')
        price = request.POST.get('variantPrice')
        if not price:
            messages.error(request, "Narx majburiy")
            return redirect('menu:edit_food', food_id=food_id)
        image = request.FILES.get('variantImage')
        if not image:
            image = food.image
        variant = FoodVariant.objects.create(
            food=food,
            name=name,
            description=description,
            price=price,
            image=image
        )
        food.has_variants = True
        food.save()
        messages.success(request, "Taom turi qo'shildi!")
        return redirect('menu:edit_food', food_id=food_id)
    messages.error(request, "GET metod ruxsat berilmagan!")
    return redirect('menu:edit_food', food_id=food_id)


@only_kitchen
def delete_food_variant(request, variant_id):
    food_variant = get_object_or_404(FoodVariant, id=variant_id)
    try:
        food_variant.delete()
    except Exception as err:
        logging.error(err)
        messages.error(request, "Nimadir xato...!")
    messages.success(request, "Taom turi o'chirildi!")
    return redirect('menu:edit_food', food_id=food_variant.food.id)

