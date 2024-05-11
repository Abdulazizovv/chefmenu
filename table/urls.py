from django.urls import path
from .views import (
    index,
    delete_table,
    edit_table
    )


app_name = 'table'

urlpatterns = [
    path('', index, name='index'),
    path('delete/', delete_table, name='delete'),
    path('edit/', edit_table, name='edit'),
]
