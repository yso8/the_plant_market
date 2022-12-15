from django.urls import path

# import all functions defined
from . import views
from .views import account_home, account_address, account_order, account_return

app_name = 'my_account'
urlpatterns = [
    # ex : /my-account/
    path('account/', account_home, name='home'),
    path('account/addresses', account_address, name='addresses'),
    path('account/orders', account_order, name='orders'),
    path('account/returns', account_return, name='returns')
]
