import json

from django.core.management import BaseCommand

from catalog.models import Product, Category


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open('fixture/category_data.json', encoding="utf-8") as f:
            json_data = json.load(f)
            categories = []
            for data in json_data:
                categories.append(data['fields'])
            return categories

    @staticmethod
    def json_read_products():
        with open('fixture/product_data.json', encoding="utf-8") as f:
            json_data = json.load(f)
            products = []
            for data in json_data:
                products.append(data['fields'])
            return products

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        product_for_create = []
        category_for_create = []

        for category in Command.json_read_categories():
            category_for_create.append(Category(**category))

        Category.objects.bulk_create(category_for_create)

        for product in Command.json_read_products():
            product_for_create.append(
                Product(name=product['name'],
                        description=product['description'],
                        category=Category.objects.get(name='яблоки'),
                        price=product['price'])
            )

        Product.objects.bulk_create(product_for_create)
