from django import forms
from phonenumber_field.formfields import PhoneNumberField


class AddressForm(forms.Form):
    name = forms.CharField(max_length=100)
    city = forms.CharField(max_length=38)
    postal_code = forms.CharField(max_length=5)
    address_complement = forms.CharField(max_length=50, required=False)
