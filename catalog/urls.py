from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.views import ProductListView, ContactTemplateView, ProductDetailView, ProductCreateView, BlogListView, \
    BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView, ProductUpdateView, ProductDeleteView
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contact/', ContactTemplateView.as_view(), name='contact'),
    path('product/<int:pk>', cache_page(60)(ProductDetailView.as_view()), name='product'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('product_update/<int:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('product_delete/<int:pk>', ProductDeleteView.as_view(), name='product_delete'),
    path('blogs/', BlogListView.as_view(), name='blogs'),
    path('blog/<int:pk>', BlogDetailView.as_view(), name='blog'),
    path('create_blog/', BlogCreateView.as_view(), name='create_blog'),
    path('update_blog/<int:pk>', BlogUpdateView.as_view(), name='update_blog'),
    path('delete_blog/<int:pk>', BlogDeleteView.as_view(), name='delete_blog'),
]
