from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from store.views import index, product_detail, add_to_cart, cart, delete_cart, index_add_to_cart, delete_product_to_cart, add_to_favorite, select_delivery_method, payment_method
from account.views import signup, logout_user, login_user
from shop import settings

urlpatterns = [
    path('', index, name='index'),
    path('', include('account.urls')),
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name="logout"),
    path('product/<str:slug>/', product_detail, name='product_detail'),
    path('product/<str:slug>/add-to-cart/', add_to_cart, name='add-to-cart'),
    path('favorite/<int:id>/add', add_to_favorite, name="add-to-favorite"),
    path('cart/', cart, name="cart"),
    path('index-add-to-cart/<str:slug>/', index_add_to_cart, name="index-add-to-cart"),
    path('cart/delete-product/<str:slug>/', delete_product_to_cart, name="delete-product-to-cart"),
    path('cart/delivery', select_delivery_method, name="address_delivery_selection"),
    path('payment', payment_method, name="payment")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
