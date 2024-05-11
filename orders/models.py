import uuid
from django.db import models
from main.models import Food
from users.models import User, Kitchen
from table.models import Table
from datetime import datetime
import random


class OrderItems(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    total_price = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.food} - {self.quantity}'
    
    def save(self, *args, **kwargs):
        self.price = self.food.price
        self.total_price = self.price * self.quantity
        super(OrderItems, self).save(*args, **kwargs)



class Orders(models.Model):
    order_status = [
        ('new', 'Yangi'),
        ('in_progress', 'Ishlanmoqda'),
        ('done', 'Bajarildi'),
    ]
    order_id = models.CharField(max_length=10, unique=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=10, unique=True, editable=False)
    kitchen = models.ForeignKey(Kitchen, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    foods = models.ManyToManyField(OrderItems)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.IntegerField()
    status = models.CharField(max_length=20, choices=order_status, default='new')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Order #{self.id}'
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generating a unique order id based on timestamp and a random number
            timestamp = int(datetime.now().timestamp())  # Get current timestamp
            random_number = random.randint(10000, 99999)  # Generate a random number
            self.order_number = f'{timestamp}{random_number}'  # Combine timestamp and random number
        super().save(*args, **kwargs)
    

    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'



