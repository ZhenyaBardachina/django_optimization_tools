from django.conf import settings
from django.test import TestCase
from authapp.models import ShopUser
from django.test.client import Client


class UserManagementTestCase(TestCase):
    username = 'django'
    email = 'django@geekshop.local'
    password = 'geekbrains'
    status_code_success = 200
    status_code_redirect = 302

    new_user_data = {
        'username': 'django01',
        'first_name': 'Django',
        'last_name': 'Django',
        'password1': 'geekbrains',
        'password2': 'geekbrains',
        'age': 33,
        'email': 'django1@gb.local'
    }

    def setUp(self):
        self.user = ShopUser.objects.create_superuser('django', email=self.email, password=self.password)
        self.client = Client()

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertTrue(response.context['user'].is_anonymous)

        # данные пользователя
        self.client.login(username=self.username, password=self.password)
        # логинимся
        response = self.client.get('/auth/user/login/')
        # self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.status_code, self.status_code_redirect)

    def test_user_register(self):
        response = self.client.post('/auth/register/', data=self.new_user_data)
        self.assertEqual(response.status_code, self.status_code_redirect)

        new_user = ShopUser.objects.get(username=self.new_user_data['username'])

        activation_url = f'{settings.DOMAIN_NAME}/auth/verify/{new_user.email}/{new_user.activation_key}/'

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, self.status_code_success)

        new_user.refresh_from_db()
        self.assertTrue(new_user.is_active)

    def test_basket_login_redirect(self):
        # без логина должен переадресовать
        response = self.client.get('/basket/')
        self.assertEqual('/auth/login/?next=/basket/', response.url)
        self.assertEqual(302, response.status_code)

        # с логином все должно быть хорошо
        self.client.login(username='Zhenya', password='geekbrains')

        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, self.status_code_redirect)
        self.assertEqual([], list(response.context['user'].basket_items))
        self.assertEqual('/basket/', response.request['PATH_INFO'])
        self.assertIn('Ваша корзина,', response.content.decode('utf-8'))







