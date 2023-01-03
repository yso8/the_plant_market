from django.test import TestCase
from .models import Product, Category, Delivery, Shopper, Cart, CartProduct, Order, OrderProduct, OrderDetails


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
        Order.objects.create(order=cart, price=100, user=user)

        # Populate the order with products
        OrderProduct.objects.create()
        OrderProduct.objects.create()
        OrderProduct.objects.create()

        # Populate the carrier and delivery method chosen

