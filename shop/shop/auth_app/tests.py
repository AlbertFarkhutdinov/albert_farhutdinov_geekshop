from django.test import TestCase
from django.test.client import Client
from shop.auth_app.models import ShopUser
from django.core.management import call_command
from django.conf import settings


class TestUserManagement(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()
        self.superuser = ShopUser.objects.create_superuser('django2', 'django2@geekshop.local', 'geekbrains')
        self.user = ShopUser.objects.create_user('test_user', 'test_user@geekshop.local', 'unbreakable')
        self.user_with__first_name = ShopUser.objects.create_user('far', 'albert_f@ya.ru', 'new_password',
                                                                  first_name='Альберт')

    def test_user_login(self):
        # тест главной страницы без логина
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'Home page')
        self.assertNotContains(response, 'Пользователь', status_code=200)
        self.assertNotIn('Пользователь', response.content.decode())

        # Данные пользователя
        self.client.login(username='test_user', password='unbreakable')
        # Логинимся
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)
        # Главная после логина
        response = self.client.get('/')
        self.assertContains(response, 'Пользователь', status_code=200)
        self.assertEqual(response.context['user'], self.user)
        self.assertIn('Пользователь', response.content.decode())

    def test_basket_login_redirect(self):
        # Без логина должен переадресовать
        response = self.client.get('/basket/')
        self.assertEqual(response.url, '/auth/login/?next=/basket/')
        self.assertEqual(response.status_code, 302)
        # с логином все должно быть хорошо
        self.client.login(username='test_user', password='unbreakable')
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['auth_app_context']['basket_items']), [])
        self.assertEqual(response.request['PATH_INFO'], '/basket/')
        self.assertIn('В корзине ', response.content.decode())

    def test_user_logout(self):
        self.client.login(username='test_user', password='unbreakable')
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)
        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

    def test_user_register(self):
        # логин без данных пользователя
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'Регистрация')
        self.assertTrue(response.context['user'].is_anonymous)
        new_user_data = {
            'username': 'samuel',
            'first_name': 'Сэмюэл',
            'last_name': 'Джексон',
            'password1': 'sam_awesome',
            'password2': 'sam_awesome',
            'email': 'samuel@geekshop.local',
            'age': '21'}
        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 302)
        new_user = ShopUser.objects.get(username=new_user_data['username'])
        activation_url = f"{settings.DOMAIN_NAME}/auth/verify/{new_user_data['email']}/{new_user.activation_key}/"
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)
        self.client.login(username=new_user_data['username'], password=new_user_data['password1'])
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)
        response = self.client.get('/')
        self.assertContains(response, text=new_user_data['first_name'], status_code=200)

    def test_user_wrong_register(self):
        new_user_data = {
            'username': 'teen',
            'first_name': 'Мэри',
            'last_name': 'Поппинс',
            'password1': 'forever_young',
            'password2': 'forever_young',
            'email': 'merypoppins@geekshop.local',
            'age': '17'}

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'register_form', 'age', 'Вы слишком молоды!')

    def tearDown(self):
        call_command('sqlsequencereset', 'main_app', 'auth_app', 'orders_app', 'basket_app')
