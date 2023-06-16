from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from shop.settings import AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    picture = models.ImageField(upload_to='img', blank=False, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})


class Shopper(AbstractUser):
    favorite = models.ManyToManyField(Product)


class Delivery(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    time_days = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} : {self.price} {self.time_days}"


class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=256, null=True)
    carrier = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.username


    def getUserCartAndProducts(user):
        get_cart = Cart.objects.get(user=user)
        cart_articles = CartProduct.objects.filter(user_cart=get_cart)
        return cart_articles


    def getTotalCartPrice(user):
        cart_articles = Cart.getUserCartAndProducts(user)
        total = 0
        for i in cart_articles:
            # Get the product to access its value price
            get_product = Product.objects.get(id=i.product_id)
            get_product.quantity = i.quantity
            # Calculate the price based on quantity and price
            total += get_product.price * i.quantity
        return total

    def getProductsLength(cart_articles):
        return len(cart_articles)


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    user_cart = models.ForeignKey(Cart, on_delete=models.CASCADE)


class Order(models.Model):
    order = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    price = models.FloatField()
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class OrderDetails(models.Model):
    address = models.CharField(max_length=256)
    carrier = models.CharField(max_length=100)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True)
    total = models.FloatField()
