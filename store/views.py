from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from store.models import Product, Cart, Order, Delivery, Category
from account.models import Shopper
from account.models import Address
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import PaymentForm


def index(request):
    # get all the products in the database
    products = Product.objects.all()
    # get all the filters which are the category of the products
    filters = Category.objects.all()
    return render(request, 'store/index.html', context={"products": products, "filters": filters})


def filter_products(request, filter):
    category = Category.objects.get(name=filter)
    print(category.id)
    products = Product.objects.filter(category=category.id)
    filters = Category.objects.all()
    return render(request, 'store/index.html', context={"products": products, "filters": filters})


def product_detail(request, slug):
    # get only the information about the selected product
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
    # get user cart
    get_cart = get_object_or_404(Cart, user=request.user)
    cart_articles = Order.objects.filter(user=request.user.id)
    # initialize a value to calculate the total before shipment fees
    total = 0
    # loop through the cart
    for i in cart_articles:
        # Get the product to access its value price
        get_product = Product.objects.get(id=i.product_id)
        # Calculate the price based on quantity and price
        total += get_product.price * i.quantity

    # set the total price on the database
    #cart_articles.price = total
    #cart_articles.save()

    return render(request, 'store/cart.html', context={"orders": get_cart.orders.all(), "total": total})


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
    # load all the favorites from the logged user
    favorites = Shopper.objects.filter(id=request.user.id)

    for i in favorites:
        print(i.favorite)
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
    if request.method == 'POST':
        address_name = request.POST.get("address_name")
        carrier_name = request.POST.get("carrier_name")
        return HttpResponseRedirect('/payment')

    addresses = Address.objects.filter(user=request.user)
    deliveries = Delivery.objects.all()
    return render(request, 'store/address_delivery_selector.html', context={"addresses": addresses,
                                                                            "deliveries": deliveries})


@login_required
def payment_method(request):
    # if the request is post
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        # if the form is valid
        if form.is_valid():
            # get the values from each field
            name = form.cleaned_data['name']
            card = form.cleaned_data['card_number']
            expiration = form.cleaned_data['expiration_date']
            cvv = form.cleaned_data['cvv']

            print(name, card, expiration, cvv)
            if name == "Admin admin" and card == '1234567812345678' and expiration == "12/22" and cvv == "123":
                return HttpResponseRedirect('/payment/successful')
            else:
                error = True
                return render(request, 'store/payment.html', {'form': form, 'error': error})
    # if the request is a get
    else:
        # load the form created in forms.py
        form = PaymentForm()
        return render(request, 'store/payment.html', {'form': form})


def handle_not_found(request, exception):
    return render(request, 'error/404.html')
