import json
from datetime import datetime

from django.core.management import BaseCommand

from catalog.models import Product, Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()

        with open('./data.json', 'r') as f:
            the_list = json.loads(f.read())

        categories_to_fill = []
        products_to_fill = []
        index_for_products = {}
        for item in the_list:
            if item['model'] == 'catalog.category':
                temp = Category(**item['fields'])
                categories_to_fill.append(temp)
                index_for_products |= ({item['pk']: temp})
            elif item['model'] == 'catalog.product':
                products_to_fill.append(Product(name=item['fields']['name'],
                                                description=item['fields']['description'],
                                                image=item['fields']['image'],
                                                price=item['fields']['price'],
                                                creation_date=item['fields']['creation_date'],
                                                update_date=item['fields']['update_date'],
                                                category=index_for_products[item['fields']['category']]))
        Category.objects.bulk_create(categories_to_fill)
        Product.objects.bulk_create(products_to_fill)

