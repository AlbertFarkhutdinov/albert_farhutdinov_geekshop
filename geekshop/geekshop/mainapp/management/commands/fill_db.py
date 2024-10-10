from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
from authapp.models import ShopUser
from configparser import RawConfigParser
from django.conf import settings
import json
import os
JSON_PATH = 'json'
local_config_path = os.path.join(settings.BASE_DIR, 'conf', 'local.conf')
config = RawConfigParser()
config.read(local_config_path)


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')
        ProductCategory.objects.all().delete()
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()

        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            category_name = product["category"]
            # Получаем категорию по имени
            _category = ProductCategory.objects.get(name=category_name)
            # Заменяем название категории объектом
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        # Создаем суперпользователя при помощи менеджера модели
        ShopUser.objects.all().delete()
        ShopUser.objects.create_superuser(username=config.get('superuser', 'username'),
                                          email=config.get('superuser', 'email'),
                                          password=config.get('superuser', 'password'),
                                          age=config.getint('superuser', 'age'),
                                          first_name=config.get('superuser', 'first_name')
                                          )
