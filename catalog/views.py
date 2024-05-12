from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from catalog.forms import ArticlesForm
from catalog.models import Product


def home(request):
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 3)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {
        'page_obj': page_obj,
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
        'object_list': prod,
    }

    return render(request, 'catalog/product.html', context)


def create(request):
    error = ''
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalog:home')
        else:
            error = 'Форма заполнена неверно'
    form = ArticlesForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'catalog/create.html', context)
