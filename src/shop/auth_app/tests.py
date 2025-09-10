from django.conf import settings
from django.core.management import call_command
from django.test import TestCase
from django.test.client import Client

from shop.auth_app.models import ShopUser

USERNAME = 'username'
USER = 'User'
TEST_USER = 'test_user'
TEST_PSW = 'unbreakable'


class TestUserManagement(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()
        self.superuser = ShopUser.objects.create_superuser(
            username='django2',
            email='django2@geekshop.local',
            password='geekbrains',
        )
        self.user = ShopUser.objects.create_user(
            username=TEST_USER,
            email='test_user@geekshop.local',
            password=TEST_PSW,
        )
        self.user_with_first_name = ShopUser.objects.create_user(
            username='far',
            email='albert_f@ya.ru',
            password='new_password',
            first_name='Albert',
        )

    def test_user_login(self):
        """Test main page without login."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        user = response.context['user']
        self.assertTrue(user.is_anonymous)
        self.assertEqual(response.context['title'], 'Home page')
        self.assertNotContains(response, USER, status_code=200)
        self.assertNotIn(USER, response.content.decode())

        self.client.login(username=TEST_USER, password=TEST_PSW)
        response = self.client.get('/auth/login/')
        self.assertFalse(user.is_anonymous)
        self.assertEqual(user, self.user)
        response = self.client.get('/')
        self.assertContains(response, USER, status_code=200)
        self.assertEqual(user, self.user)
        self.assertIn(USER, response.content.decode())

    def test_basket_login_redirect(self):
        response = self.client.get('/basket/')
        self.assertEqual(response.url, '/auth/login/?next=/basket/')
        self.assertEqual(response.status_code, 302)
        self.client.login(username=TEST_USER, password=TEST_PSW)
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            first=list(response.context['auth_app_context']['basket_items']),
            second=[],
        )
        self.assertEqual(response.request['PATH_INFO'], '/basket/')
        self.assertIn('In basket ', response.content.decode())

    def test_user_logout(self):
        self.client.login(username=TEST_USER, password=TEST_PSW)
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        user = response.context['user']
        self.assertFalse(user.is_anonymous)
        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.is_anonymous)

    def test_user_register(self):
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'Registration')
        user = response.context['user']
        self.assertTrue(user.is_anonymous)
        new_user_data = {
            USERNAME: 'samuel',
            'first_name': 'Samuel',
            'last_name': 'Jackson',
            'password1': 'sam_awesome',
            'password2': 'sam_awesome',
            'email': 'samuel@geekshop.local',
            'age': '21',
        }
        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 302)
        new_user = ShopUser.objects.get(username=new_user_data[USERNAME])
        activation_url = '/'.join(
            [
                settings.DOMAIN_NAME,
                'auth',
                'verify',
                new_user_data['email'],
                new_user.activation_key,
                '',
            ],
        )
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)
        self.client.login(
            username=new_user_data[USERNAME],
            password=new_user_data['password1'],
        )
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(user.is_anonymous)
        response = self.client.get('/')
        self.assertContains(
            response=response,
            text=new_user_data['first_name'],
            status_code=200,
        )

    def test_user_wrong_register(self):
        new_user_data = {
            USERNAME: 'teen',
            'first_name': 'Mary',
            'last_name': 'Poppins',
            'password1': 'forever_young',
            'password2': 'forever_young',
            'email': 'merypoppins@geekshop.local',
            'age': '17',
        }

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            form=response,
            field='register_form',
            errors='age',
            msg_prefix='You are too young!',
        )

    def tearDown(self):
        call_command(
            'sqlsequencereset',
            'main_app',
            'auth_app',
            'orders_app',
            'basket_app',
        )
