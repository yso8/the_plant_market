from django.test import TestCase
from .models import Product, Category, Delivery


class ProductModelTests(TestCase):
    def test_create_product(self):
        product = Product()
        product.save()
        user = Product.objects.get(username='user', email='user@user.com', password='root')
        self.assertEqual(user.email, 'user@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


class CategoryModelTests(TestCase):
    def test_create_category(self):
        category = Category(name="Arbres")
        category.save()
        self.assertEqual(category.name, "Arbres")


class DeliveryModelTests(TestCase):
    def test_create_carrier(self):
        carrier = Delivery(name="UPS", price=10, time_days="1-2")
        carrier.save()
        get_carrier = Delivery.objects.get(name="UPS").first()
        self.assertEqual(get_carrier.name, "UPS")
        self.assertEqual(get_carrier.price, 10)
        self.assertEqual(get_carrier.time_days, "1-2")
