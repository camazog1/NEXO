from django import forms
from .models import Product, ProductImage
from django.utils.translation import gettext_lazy as _

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'reference', 'description', 'price', 'price_dolar', 'is_popular', 'is_new', 'discontinued']
        labels = {
            'title': _('Title'),
            'reference': _('Reference'),
            'description': _('Description'),
            'price': _('Price (COP)'),
            'price_dolar': _('Price (USD)'),
            'is_popular': _('Popular Product'),
            'is_new': _('New Product'),
            'discontinued': _('Discontinued Product'),
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(),
        }
        labels = {
            'image': _('Product Image'),
        }