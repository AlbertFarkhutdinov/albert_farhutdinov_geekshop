# from django.test import TestCase
# from django.test.client import Client
# from shop.main_app.models import Product, ProductCategory
# from django.core.management import call_command
#
#
# class TestMainAppSmoke(TestCase):
#     def setUp(self):
#         call_command('flush', '--noinput')
#         call_command('loaddata', 'test_db.json')
#         self.client = Client()
#
#     def test_main_app_urls(self):
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)
#         response = self.client.get('/contacts/')
#         self.assertEqual(response.status_code, 200)
#         response = self.client.get('/products/')
#         self.assertEqual(response.status_code, 200)
#         response = self.client.get('/products/category/0/')
#         self.assertEqual(response.status_code, 200)
#         for category in ProductCategory.objects.all():
#             response = self.client.get(f'/products/category/{category.pk}/')
#             self.assertEqual(response.status_code, 200)
#         for product in Product.objects.all():
#             response = self.client.get(f'/products/product/{product.pk}/')
#             self.assertEqual(response.status_code, 200)
#
#    def tearDown(self):
#        call_command(
#            'sqlsequencereset',
#            'main_app',
#            'auth_app',
#            'orders_app',
#            'basket_app',
#        )
