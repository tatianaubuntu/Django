from .models import Product
from django.forms import ModelForm, TextInput, ImageField, Select, Textarea, FloatField


class ArticlesForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'image',
            'category',
            'price',
        ]

