from django.contrib.auth.models import AbstractUser
from phonenumber_field.formfields import PhoneNumberField
from django.db import models


class Shopper(AbstractUser):
    city = models.CharField(max_length=38, blank=False),
    phone_number = PhoneNumberField(region="FR"),
    postal_code = models.CharField(max_length=5),
    address_complement = models.CharField(max_length=50, blank=True)
