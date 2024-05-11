from django.urls import path

from catalog.views import home, contact, product

app_name = 'catalog'

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contact, name='contact'),
    path('product/<int:pk>', product, name='product'),
]
