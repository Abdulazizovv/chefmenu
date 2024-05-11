from django.urls import path
from .views import (
    index, 
    register, 
    login_, 
    logout_, 
    kitchen_detail, 
    kitchen_foods, 
    register_kitchen, 
    redirect_menu, 
    kitchen_profile, 
    user_profile, 
    about,
    kitchen_info,
    kitchen_user_profile,
    contact,
)


app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name="about"),
    path('contact/', contact, name="contact"),
    path('kitchen/kitchen-profile/', kitchen_profile, name='kitchen_profile'),
    path('kitchen/user/profile/', kitchen_user_profile, name='kitchen_user_profile'),
    path('kitchen/<slug:kitchen_slug>/', kitchen_info, name='kitchen_info'),
    path('user/profile/', user_profile, name='user_profile'),
    path('menu/<slug:slug>/', kitchen_detail, name="menu"),
    path('menu/<slug:slug>/foods/', kitchen_foods, name="foods"),
    path('menu/<str:kitchen_id>/<str:table_id>/', redirect_menu, name='redirect'),
    path('register/', register, name='register'),
    path('register-kitchen/', register_kitchen, name='register_kitchen'),
    path('login/', login_, name='login'),
    path('logout/', logout_, name='logout'),
]
