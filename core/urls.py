from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('kitchen/menu/', include('menu.urls')),
    path('kitchen/tables/', include('table.urls')),
    path('cart/', include('cart.urls')),
    path('verification/', include('verification.urls')),
    path('reviews/', include('reviews.urls')),
    path('orders/', include('orders.urls')),
    path('', include('main.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)