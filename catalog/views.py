from django.shortcuts import render

from catalog.models import Product


def home(request):
    products_list = Product.objects.all()
    context = {
        'object_list': products_list
    }
    return render(request, 'catalog/home.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'You have new message from {name} (tel: {phone}): {message}')
    return render(request, 'catalog/contact.html')


def product(request, pk):
    prod = Product.objects.get(pk=pk)
    context = {
        'object_list': prod
    }

    return render(request, 'catalog/product.html', context)
