from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from store.views import index, product_detail, add_to_cart, cart, delete_cart, index_add_to_cart, delete_product_to_cart
from accounts.views import signup, logout_user, login_user
from shop import settings

urlpatterns = [
                  path('', index, name='index'),
                  path('admin/', admin.site.urls),
                  path('signup/', signup, name='signup'),
                  path('login/', login_user, name='login'),
                  path('logout/', logout_user, name="logout"),
                  path('product/<str:slug>/', product_detail, name='product_detail'),
                  path('product/<str:slug>/add-to-cart/', add_to_cart, name='add-to-cart'),
                  path('cart/', cart, name="cart"),
                  path('index-add-to-cart/<str:slug>/', index_add_to_cart, name="index-add-to-cart"),
                  path('cart/delete-product/<str:slug>/', delete_product_to_cart, name="delete-product-to-cart"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
