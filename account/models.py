from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.formfields import PhoneNumberField

class Shopper(AbstractUser):
    pass


class Address(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=38, default='default')
    postal_code = models.CharField(max_length=5)
    address_complement = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(Shopper, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
