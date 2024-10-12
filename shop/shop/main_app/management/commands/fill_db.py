from django.core.management.base import BaseCommand
from shop.main_app.models import ProductCategory, Product
from shop.auth_app.models import ShopUser
from configparser import RawConfigParser
from django.conf import settings
import json


JSON_PATH = settings.JSON_DIR
local_config_path = settings.CONF_DIR.joinpath('local.conf')
config = RawConfigParser()
config.read(local_config_path)


def load_from_json(file_name):
    with JSON_PATH.joinpath(file_name).with_suffix('.json').open() as infile:
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
            _category = ProductCategory.objects.get(name=category_name)
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        ShopUser.objects.all().delete()
        section_name = 'superuser'
        ShopUser.objects.create_superuser(
            username=config.get(section=section_name, option='username'),
            email=config.get(section=section_name, option='email'),
            password=config.get(section=section_name, option='password'),
            age=config.getint(section=section_name, option='age'),
            first_name=config.get(section=section_name, option='first_name'),
        )
