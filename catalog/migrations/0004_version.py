# Generated by Django 5.0.6 on 2024-05-29 10:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_blog'),
    ]

    operations = [
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_num', models.IntegerField(default=0, verbose_name='номер версии')),
                ('version_name', models.CharField(max_length=150, verbose_name='название версии')),
                ('is_active', models.BooleanField(default=True, verbose_name='активно')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='продукт')),
            ],
        ),
    ]
