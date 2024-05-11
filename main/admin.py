from django.contrib import admin
from .models import Food, FoodVariant, Menu, FoodCategory, ContactMessages
from django.utils.text import slugify
from .utils import resize_image





class FoodCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            base_slug = slugify(obj.title)
            slug = base_slug
            counter = 1
            while FoodCategory.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            obj.slug = slug
        super().save_model(request, obj, form, change)


class FoodAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Call the original save_model method to save the object
        super().save_model(request, obj, form, change)
        
        # Resize the image if it's being added or changed
        if 'image' in form.changed_data or not change:
            resize_image(obj.image, 300, 300)


admin.site.register(FoodCategory, FoodCategoryAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(FoodVariant)
admin.site.register(Menu)
admin.site.register(ContactMessages)