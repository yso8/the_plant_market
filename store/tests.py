from django.test import TestCase
from .models import Product, Category, Delivery, Shopper, Cart, CartProduct, Order, OrderProduct, OrderDetails
from account.models import Address
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver


class ProductModelTests(TestCase):
    def test_create_product_modify_delete(self):
        # Create new product
        # (must create a category before adding a product)
        category = Category(name="monocotylédones")
        category.save()
        product = Product(name="Orchidée blanche", slug="orchidée-blanche", price=20, quantity=5
                          , description="Pellentesque cursus ligula ipsum. Aliquam erat volutpat. "
                                        "Nullam convallis tellus risus.", picture="image.png", category=category)
        # Make sure the assertion is correct
        self.assertEqual(product.name, "Orchidée blanche")
        self.assertEqual(product.slug, "orchidée-blanche")

        # Modify the slug of the product
        product.slug = "orchidée-white"
        product.save()
        self.assertEqual(product.slug, "orchidée-white")

        # Delete the product
        product.delete()
        self.assertFalse(Product.objects.filter(name="Orchidée blanche").exists())


class CategoryModelTests(TestCase):
    def test_create_category(self):
        category = Category(name="Arbres")
        category.save()
        self.assertEqual(category.name, "Arbres")


class DeliveryModelTests(TestCase):
    # Create a new carrier
    def test_create_carrier(self):
        carrier = Delivery(name="UPS", price=10, time_days="1-2")
        carrier.save()
        # Query to get the new added the carrier
        get_carrier = Delivery.objects.get(name="UPS")
        self.assertEqual(get_carrier.name, "UPS")
        self.assertEqual(get_carrier.price, 10)
        self.assertEqual(get_carrier.time_days, "1-2")

    def test_delete_carrier(self):
        carrier = Delivery(name="DHL", price=10, time_days="1-2")
        carrier.save()
        carrier.delete()
        self.assertFalse(Delivery.objects.filter(name="DHL").exists())


class CartModelTests(TestCase):

    # Simulate add products in the cart
    def test_add_product_cart(self):
        # Create a new user
        user = Shopper.objects.create_user(username='user', email='user@user.com', password='root')

        # Create the cart associated to the user
        cart = Cart(user=user, address="Temporary address", carrier="DHL")
        cart.save()

        # Create news category for the products
        category1 = Category(name="Plantes d'intérieures")
        category2 = Category(name="Plantes extérieures")
        category1.save()
        category2.save()

        # Create news products
        product1 = Product(name="Orchidée blanche", slug="orchidee-blanche", price=20, quantity=10,
                           description="Orchidée blanche d'intérieur", picture="orchibla.png", category=category1)
        product2 = Product(name="Cactus", slug="cactus", price=20, quantity=8,
                           description="Cactus extérieure",
                           picture="cactus.png", category=category2)
        product3 = Product(name="Orchidée violette", slug="orchidee-violette", price=20, quantity=7,
                           description="Orchidée violette d'intérieur", picture="orchivio.png", category=category2)
        product1.save()
        product2.save()
        product3.save()

        # Add products to the cart
        cart_product1 = CartProduct(product=product1, quantity=2, user_cart=cart)
        cart_product2 = CartProduct(product=product2, quantity=3, user_cart=cart)
        cart_product1.save()
        cart_product2.save()

        get_cart_products = CartProduct.objects.filter(user_cart=cart)
        self.assertEqual(get_cart_products[0].product.name, "Orchidée blanche")
        self.assertEqual(get_cart_products[1].product.name, "Cactus")

        # test length of the cart corresponding to the two products in the cart
        self.assertEqual(get_cart_products.count(), 2)


class OrderModelTests(TestCase):

    def test_create_order(self):
        user = Shopper.objects.create_user(username='user', email='user@user.com', password='root')
        cart = Cart(user=user, address="Temporary address", carrier="DHL")
        cart.save()

        # Create news category for the products
        category1 = Category(name="Plantes d'intérieures")
        category2 = Category(name="Plantes extérieures")
        category1.save()
        category2.save()

        # Create news products
        product1 = Product(name="Orchidée blanche", slug="orchidee-blanche", price=20, quantity=10,
                           description="Orchidée blanche d'intérieur", picture="orchibla.png", category=category1)
        product2 = Product(name="Cactus", slug="cactus", price=20, quantity=8,
                           description="Cactus extérieure",
                           picture="cactus.png", category=category2)
        product3 = Product(name="Orchidée violette", slug="orchidee-violette", price=20, quantity=7,
                           description="Orchidée violette d'intérieur", picture="orchivio.png", category=category2)
        product1.save()
        product2.save()
        product3.save()

        # Create an order from the object in the cart
        order = Order(order=cart, price=100, user=user)
        order.save()

        # Populate the order with products
        OrderProduct.objects.create(product=product1, order_id=order, quantity=2)
        OrderProduct.objects.create(product=product2, order_id=order, quantity=1)

        # Create a delivery address for the user
        address = Address(name="126 rue de Bugarelles", city="Montpellier", postal_code=34070, address_complement="",
                          user=user)

        # Create a carrier for the delivery
        carrier = Delivery(name="DHL", price=10, time_days="1-2")

        # Populate the carrier and delivery method chosen
        OrderDetails.objects.create(address=address, carrier=carrier, order=order, total=100)

        # Make sure the data insert match the one from the database

        get_order = Order.objects.get(order=cart)
        self.assertEqual(get_order.id, order.id)

        get_products = OrderProduct.objects.filter(order_id=get_order)
        self.assertEqual(get_products[0].product.name, product1.name)
        self.assertEqual(get_products[1].product.name, product2.name)
        self.assertFalse(OrderProduct.objects.filter(id=3).exists())

        # Check the delivery options
        get_delivery = OrderDetails.objects.get(order=order)
        self.assertEqual(get_delivery.address, "126 rue de Bugarelles")
        self.assertEqual(get_delivery.carrier, "DHL : 10 1-2")

        # self.assertEqual(Delivery.objects.get())


# Functional tests
class MySeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('louis')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('root')
        self.selenium.find_element(By.XPATH, '//button[text()="Login"]')

    # def test_register(self):
