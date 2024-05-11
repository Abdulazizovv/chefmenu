from django.contrib import admin
from django.utils.text import slugify
from .models import User, Kitchen, PhoneNumbers, SocialLinks, EmployeeProfile, UserProfile


class KitchenAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            base_slug = slugify(obj.title)
            slug = base_slug
            counter = 1
            while Kitchen.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            obj.slug = slug
        super().save_model(request, obj, form, change)



admin.site.register(User)
admin.site.register(Kitchen, KitchenAdmin)
admin.site.register(PhoneNumbers)
admin.site.register(SocialLinks)
admin.site.register(EmployeeProfile)
admin.site.register(UserProfile)
