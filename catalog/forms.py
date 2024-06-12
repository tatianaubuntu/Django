from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, BaseInlineFormSet

from .models import Product, Version


class ProductForm(ModelForm):
    forbidden_words = ['казино',
                       'криптовалюта',
                       'крипта',
                       'биржа',
                       'дешево',
                       'бесплатно',
                       'обман',
                       'полиция',
                       'радар']

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'image',
            'category',
            'price',
        ]

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        for forbidden_word in self.forbidden_words:
            if forbidden_word in cleaned_data.lower():
                raise forms.ValidationError('Присутствует запрещенное слово')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        for forbidden_word in self.forbidden_words:
            if forbidden_word in cleaned_data.lower():
                raise forms.ValidationError('Присутствует запрещенное слово')

        return cleaned_data


class ProductModerator1Form(ModelForm):
    class Meta:
        model = Product
        fields = [
            'description',
            'category',
            'is_published',
            ]


class ProductModerator2Form(ModelForm):
    class Meta:
        model = Product
        fields = [
            'description',
            'category',
            ]


class VersionForm(ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

    # def clean_is_active(self):
    #     cleaned_data = self.cleaned_data.get('is_active')
    #     version = Version.objects.filter(product=self.cleaned_data.get('product'), is_active=True).exists()
    #     if cleaned_data and version:
    #         raise forms.ValidationError('Активная версия уже существует')
    #     # return cleaned_data


class BaseVersionInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        active_count = 0
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False) and form.cleaned_data.get('is_active', False):
                active_count += 1
        if active_count > 1:
            raise ValidationError('Может быть только одна активная версия.')
