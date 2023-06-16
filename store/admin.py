from django.contrib import admin
from .models import Product, Order, Cart, Delivery, Category, CartProduct

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Delivery)
admin.site.register(Category)
admin.site.register(CartProduct)