from django.urls import path

from catalog.views import home, contact

app_name = 'catalog'

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contact, name='contact'),
]
