from django.core.exceptions import ValidationError
from django.db import models
from django.forms import BaseInlineFormSet

NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    image = models.ImageField(upload_to='products/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='категория', **NULLABLE)
    price = models.FloatField(verbose_name='цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения')

    # manufactured_at = models.DateTimeField(default='1000-01-01', verbose_name='дата производства продукта')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)
    body = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog/', **NULLABLE, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    version_num = models.IntegerField(default=0, verbose_name='номер версии')
    version_name = models.CharField(max_length=150, verbose_name='название версии')
    is_active = models.BooleanField(default=True, verbose_name='активно')

    def __str__(self):
        return f'{self.is_active}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'

    # def clean(self):
    #     if self.is_active and Version.objects.filter(product=self.product, is_active=True).exists():
    #         raise ValidationError('Для каждого продукта разрешена только одна активная версия.')
    #
    # def save(self, *args, **kwargs):
    #     self.clean()
    #     super().save(*args, **kwargs)

