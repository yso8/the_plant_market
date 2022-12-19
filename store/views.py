from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from store.models import Product, Cart, Order, Delivery, Category
from account.models import Shopper
from account.models import Address
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import PaymentForm


def index(request):
    products = Product.objects.all()
    filters = Category.objects.all()
    return render(request, 'store/index.html', context={"products": products, "filters": filters})


def filter_products(request, filter):
    print(filter)
    return redirect('/login')


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', context={"product": product})


@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user, product=product)

    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1
        order.save()

    return redirect(reverse("product_detail", kwargs={"slug": slug}))


@login_required
def index_add_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user, product=product)

    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1
        order.save()

    products = Product.objects.filter()
    nb_products = len(products)
    return render(request, 'store/index.html', context={"products": products, "nb_products": nb_products})


@login_required
def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    print("Mon cart :")
    print(cart.orders)
    cart_articles = cart.orders.all()
    total = 0
    for i in cart_articles:
        total += 1
    print(total)

    return render(request, 'store/cart.html', context={"orders": cart.orders.all(), "total": total})


@login_required
def add_to_favorite(request, id):
    # get the product selected by user
    product = Product.objects.get(id=id)

    # get the current user
    user = Shopper.objects.get(id=request.user.id)
    user.favorite.add(product)

    # check if product is already in favorite


@login_required
def show_favorite(request):
    print(request.user.id)
    favorites = Shopper.objects.filter(favorite=request.user.id)
    print(favorites)
    return render(request, 'store/favorite.html', context={"favorites": favorites})


@login_required
def delete_cart(request):
    if cart := get_object_or_404(Cart, user=request.user):
        cart.orders.all().delete()
        cart.delete()
    return redirect('index')


@login_required
def delete_product_to_cart(request, slug):
    if cart := get_object_or_404(Cart, user=request.user):
        if len(cart.orders.all()) == 1:
            cart.orders.all().delete()
            cart.delete()
            return redirect('index')
        else:
            product = get_object_or_404(Product, slug=slug)
            order = get_object_or_404(Order, user=request.user, product=product)
            order.delete()
            return redirect('cart')
    else:
        return redirect('index')


@login_required
def select_delivery_method(request):
    addresses = Address.objects.filter(user=request.user)
    deliveries = Delivery.objects.all()
    return render(request, 'store/address_delivery_selector.html', context={"addresses": addresses,
                                                                            "deliveries": deliveries})


@login_required
def payment_method(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        print(form)
        if form.is_valid():
            #get the values from the form

            return HttpResponseRedirect('/payment/successful')
    else:
        form = PaymentForm()

    return render(request, 'store/payment.html', {'form': form})
