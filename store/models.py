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
