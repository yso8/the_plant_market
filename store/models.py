from django.db import models
from django.urls import reverse

from shop.settings import AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=100)


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


class Delivery(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    time_days = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} : {self.price} {self.time_days}"


class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user} : {self.product.name} ({self.quantity})"

    def total(self):
        return product


class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.user.username
