from django import forms
from phonenumber_field.formfields import PhoneNumberField


class PaymentForm(forms.Form):
    name = forms.CharField(max_length=100)
    card_number = forms.CharField(max_length=100)
    expiration_date = forms.CharField(max_length=5)
    cvv = forms.CharField(max_length=3)
