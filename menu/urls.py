from django.urls import path
from .views import (
    add_food,
    category_foods,
    kitchen_menu,
    all_foods,
    delete_category,
    edit_category,
    edit_food, edit_food_details, delete_food_variant,
    add_food_variant,
    delete_food
)


app_name = 'menu'

urlpatterns = [
    path('', kitchen_menu, name='kitchen_menu'),
    path('foods/', all_foods, name='all_foods'),
    path('add-food/', add_food, name='add_food'),
    path('add-food-variant/', add_food_variant, name='add_food_variant'),
    path('delete-food-variant/<int:variant_id>/', delete_food_variant, name='delete_food_variant'),
    path('edit-food/<int:food_id>/', edit_food, name='edit_food'),
    path('edit-food-details/', edit_food_details, name='edit_food_details'),
    path('delete-category/', delete_category, name='delete_category'),
    path('edit-category/', edit_category, name='edit_category'),
    path('delete-food/', delete_food, name='delete_food'),
    path('<slug:title>/', category_foods, name='category_foods'),

]
