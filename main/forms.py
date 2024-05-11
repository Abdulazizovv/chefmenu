from django import forms
from .models import Food, FoodVariant

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['category', 'name', 'price', 'description', 'image']

class FoodVariantForm(forms.ModelForm):
    class Meta:
        model = FoodVariant
        fields = ['name', 'price', 'description', 'image']

FoodVariantFormset = forms.inlineformset_factory(
    Food, FoodVariant, form=FoodVariantForm, extra=1, can_delete=False
)