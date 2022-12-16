from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client

class UserModelTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='user', email='user@user.com', password='root')
        self.assertEqual(user.email, 'user@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_authentication_successful(self):
        User = get_user_model()
        user = User.objects.create_user(username='user', email='user@user.com', password='root')
        c = Client()
        islogged = c.login(username='user', password='root')
        self.assertEqual(islogged, True)

    def test_authentication_failed(self):
        User = get_user_model()
        user = User.objects.create_user(username='user', email='user@user.com', password='root')
        c = Client()
        islogged = c.login(username='user', password='password')
        self.assertEqual(islogged, False)

    def test_user_new_adress(self):
        User = get_user_model()
        user = User.objects.create_user(username='user', email='user@user.com', password='root')