from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Kitchen
from django.utils.text import slugify
import uuid


class VerificationCode(models.Model):
    phone_number = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    is_verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code
    
    class Meta:
        verbose_name_plural = 'Verification Codes'
        db_table = 'verification_codes'
        ordering = ['-created']


class FoodCategory(models.Model):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=500)
    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while FoodCategory.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)



class Food(models.Model):
    category = models.ForeignKey(FoodCategory, on_delete=models.SET_NULL, related_name="food", null=True)
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='foods')
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='food/')
    rate = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    has_variants = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created', )
    
    def __str__(self) -> str:
        return self.name
    

class FoodVariant(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=255)  # e.g., "Large", "Chocolate Flavor", etc.
    price = models.PositiveIntegerField(default=0)  # Price for this variant
    description = models.TextField(blank=True, null=True)  # Description for this variant, optional
    image = models.ImageField(upload_to='food/variants/', blank=True, null=True)  # Image for this variant, optional

    def __str__(self):
        return f"{self.food.name} - {self.name}"


class Menu(models.Model):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='menus')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    foods = models.ManyToManyField(Food, related_name='menus')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    


class Payment(models.Model):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.SET_NULL, null=True)
    amount = models.PositiveBigIntegerField(default=0)
    is_accepted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'To`lovlar'
        ordering = ['created']
    
    def __str__(self) -> str:
        return str(f'{self.kitchen.title} - {self.amount} sum')
    

class ContactMessages(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Xabarlar'
        ordering = ['-created']
    
    def __str__(self) -> str:
        return self.name




@receiver(post_save, sender=Kitchen)
def create_kitchen_menu(sender, instance, created, **kwargs):
    if created:
        Menu.objects.create(kitchen=instance, name=f"{instance.title}'s Menu")
    
