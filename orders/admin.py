from django.contrib import admin
from .models import Orders, OrderItems


admin.site.register(Orders)
admin.site.register(OrderItems)