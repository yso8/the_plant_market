from django.urls import path

# import all functions defined
from . import views
from .views import account_home, account_address, account_order, account_return, account_address_add, account_address_update,account_address_delete
from django.contrib.auth import views as auth_views

app_name = 'my_account'
urlpatterns = [
    # ex : /my-account/
    path('account/', account_home, name='home'),
    path('account/addresses', account_address, name='addresses'),
    path('account/address/add', account_address_add, name='new_address'),
    path('account/address/update/<int:id>', account_address_update, name='update_address'),
    path('account/address/delete/<int:id>', account_address_delete, name='delete_address'),
    path('account/orders', account_order, name='orders'),
    path('account/returns', account_return, name='returns'),

    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'),
         name='password_change'),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset/password_change.html'), name='password_reset'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
         name='password_reset_complete'),
]
