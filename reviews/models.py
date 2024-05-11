from django.db import models
from users.models import User, Kitchen
from main.models import Food

# Sharhlar uchun modellar

class ReviewKitchen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kitchen = models.ForeignKey(Kitchen, on_delete=models.SET_NULL, null=True, blank=True)
    body = models.TextField()
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.body
    
    class Meta:
        verbose_name_plural = "Oshxona sharhlari"
    

class ReviewFood(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.body

    class Meta:
        verbose_name_plural = "Ovqat sharhlari"

