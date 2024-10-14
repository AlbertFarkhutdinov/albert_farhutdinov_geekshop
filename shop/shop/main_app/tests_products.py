from django.test import TestCase

from shop.main_app.models import Product, ProductCategory

PRODUCT_NAMES = ('Chair 1', 'Chair 2', 'Chair 3')


class ProductsTestCase(TestCase):
    def setUp(self):
        category = ProductCategory.objects.create(name='Chairs')
        self.products = [
            Product.objects.create(
                name=PRODUCT_NAMES[0],
                category=category,
                price=1999.5,
                quantity=150,
            ),
            Product.objects.create(
                name=PRODUCT_NAMES[1],
                category=category,
                price=2998.1,
                quantity=125,
                is_active=False,
            ),
            Product.objects.create(
                name=PRODUCT_NAMES[2],
                category=category,
                price=998.1,
                quantity=115,
            ),
        ]

    def test_product_get(self):
        for product_id, _ in enumerate(PRODUCT_NAMES[:2]):
            self.assertEqual(
                Product.objects.get(name='Chair {0}'.format(product_id + 1)),
                self.products[product_id],
            )

    def test_product_print(self):
        for product_id, _ in enumerate(PRODUCT_NAMES[:2]):
            self.assertEqual(
                str(
                    Product.objects.get(
                        name='Chair {0}'.format(product_id + 1),
                    ),
                ),
                'Chair {0} (Chairs)'.format(product_id + 1),
            )

    def test_product_get_items(self):
        product1 = Product.objects.get(name=PRODUCT_NAMES[0])
        product3 = Product.objects.get(name=PRODUCT_NAMES[2])
        products = product1.get_items()
        self.assertEqual(
            list(products),
            [product1, product3],
        )
