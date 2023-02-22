from django.test import TestCase
from django.test import Client
from .models import Address
from store.models import Shopper


class UserModelTests(TestCase):

    def test_create_user(self):
        user = Shopper.objects.create_user(username='user', email='user@user.com', password='root')
        self.assertEqual(user.email, 'user@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_authentication_successful(self):
        Shopper.objects.create_user(username='user', email='user@user.com', password='root')
        c = Client()
        islogged = c.login(username='user', password='root')
        self.assertEqual(islogged, True)

    def test_authentication_failed(self):
        Shopper.objects.create_user(username='user', email='user@user.com', password='root')
        c = Client()
        islogged = c.login(username='user', password='password')
        self.assertEqual(islogged, False)

    def test_user_add_and_get_addresses(self):
        user = Shopper.objects.create_user(username='user', email='user@user.com', password='root')
        Address.objects.create(name='Rue de la loge', city='Montpellier', postal_code=34070, user=user)
        Address.objects.create(name='Rue des condamines', city='St-Jean-de-Vedas', postal_code=34490, address_complement='Impasse', user=user)
        get_addresses = Address.objects.filter(user=user)
        self.assertEqual(get_addresses[0].name, 'Rue de la loge')
        self.assertEqual(get_addresses[1].name, 'Rue des condamines')

    def test_delete_user_address(self):
        user = Shopper.objects.create_user(username='user', email='user@user.com', password='root')
        Address.objects.create(name='Rue de la loge', city='Montpellier', postal_code=34070, user=user)
        Address.objects.filter(id=1).delete()
        self.assertFalse(Address.objects.filter(id=1).exists())
