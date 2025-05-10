from django import forms

from accounts.validators import allow_only_images_validator
from menu.models import CategoryModel, ProductModel

class CategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        fields = ['category_name', 'description']
        

class ProductItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}), validators=[allow_only_images_validator])
    class Meta:
        model = ProductModel
        fields = ['category', 'product_title', 'description', 'price', 'image', 'is_available']