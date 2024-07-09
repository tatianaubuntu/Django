from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, BaseVersionInlineFormSet, \
    ProductModerator1Form, ProductModerator2Form
from catalog.models import Product, Blog, Version, Category
from pytils.translit import slugify

from catalog.services import get_cashe_category_list, get_cashe_product_list


class ProductListView(ListView):
    """Контроллер списка продуктов"""
    model = Product
    extra_context = {
        'title': 'Главная страница'
    }
    paginate_by = 3

    def get_paginate_by(self, queryset):
        """Возвращает список продуктов по страницам"""
        return self.request.GET.get('paginate_by', self.paginate_by)

    def get_context_data(self, **kwargs):
        """Возвращает закешированный список продуктов,
        описанный в сервисной функции get_cashe_product_list()"""
        context_data = super().get_context_data(**kwargs)
        context_data['products'] = get_cashe_product_list()
        return context_data


class ContactTemplateView(TemplateView):
    """Контроллер вывода информации о контактах"""
    template_name = 'catalog/contact.html'
    extra_context = {
        'title': 'Контакты'
    }

    def get_context_data(self, **kwargs):
        if self.request.method == 'POST':
            name = self.request.POST.get('name')
            phone = self.request.POST.get('phone')
            message = self.request.POST.get('message')
            print(f'You have new message from {name} (tel: {phone}): {message}')
        return super().get_context_data(**kwargs)


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Контроллер детализации продукта"""
    model = Product
    extra_context = {
        'title': 'О продукте'
    }
    login_url = 'users:login'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        """Возвращает отображение активных версий продукта"""
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        try:
            version = Version.objects.filter(product=product, is_active=True)
        except Version.DoesNotExist:
            version = None

        context['version'] = version
        return context


class ProductCreateView(CreateView, LoginRequiredMixin):
    """Контроллер создания продукта"""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        """Создание формсета версий продукта"""
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST)
        else:
            context_data['formset'] = VersionFormset()
        return context_data

    def form_valid(self, form):
        """Сохраняет формсет и текущего пользователя как владельца продукта"""
        formset = self.get_context_data()['formset']
        self.object = form.save()
        user = self.request.user
        self.object.owner = user
        self.object.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер изменения продукта"""
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        """Направляет на указанную страницу если форма валидна"""
        return reverse('catalog:product', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        """Создание и изменение формсета версий продукта"""
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm,
                                               formset=BaseVersionInlineFormSet, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        """Сохраняет формсет версий продукта"""
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_class(self):
        """Вывод формы по изменению продукта и его версии в соответствии
        с правами пользователя"""
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return ProductForm
        elif user.has_perm('catalog.off_published') and user.has_perm('catalog.change_description') and user.has_perm('catalog.change_category'):
            if self.object.is_published:
                return ProductModerator1Form
            else:
                return ProductModerator2Form
        raise PermissionDenied


class ProductDeleteView(DeleteView, LoginRequiredMixin):
    """Контроллер удаления продукта"""
    model = Product
    success_url = reverse_lazy('catalog:home')


class BlogListView(ListView):
    """Контроллер списка блогов"""
    model = Blog
    extra_context = {
        'title': 'Блоги'
    }
    paginate_by = 3

    def get_paginate_by(self, queryset):
        """Возвращает список блогов по страницам"""
        return self.request.GET.get('paginate_by', self.paginate_by)

    def get_queryset(self, *args, **kwargs):
        """Возвращает отфильрованный список блогов по публикации"""
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    """Контроллер детализации блога"""
    model = Blog
    extra_context = {
        'title': 'О блоге'
    }

    def get_object(self, queryset=None):
        """Увеличивает количество просмотров"""
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    """Контроллер создания блога"""
    model = Blog
    fields = ('title', 'body', 'preview')
    success_url = reverse_lazy('catalog:blogs')

    def form_valid(self, form):
        """Добавляет слогифай наименованию блога"""
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    """Контроллер изменения блога"""
    model = Blog
    fields = ('title', 'body', 'preview')

    def form_valid(self, form):
        """Добавляет слогифай наименованию блога"""
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        """Направляет на указанную страницу если форма валидна"""
        return reverse('catalog:blog', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    """Контроллер удаления блога"""
    model = Blog
    success_url = reverse_lazy('catalog:blogs')


class CategoryListView(ListView):
    """Контроллер списка категорий продуктов"""
    model = Category
    extra_context = {
        'title': 'Категории'
    }

    def get_context_data(self, **kwargs):
        """Возвращает закешированный список категорий,
        описанный в сервисной функции get_cashe_category_list()"""
        context_data = super().get_context_data(**kwargs)
        context_data['categories'] = get_cashe_category_list()
        return context_data
