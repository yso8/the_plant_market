from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from store.models import Product, Cart, Order, Delivery, Category, CartProduct, OrderDetails, OrderProduct
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

    try:
        get_cart = Cart.objects.get(user=request.user)
        add_article = CartProduct(product=product, quantity=1, user_cart=get_cart)
        add_article.save()
    except Cart.DoesNotExist:
        create_cart = Cart(user=request.user)
        create_cart.save()
        add_product = CartProduct(product=product, quantity=1, user_cart=create_cart)
        add_product.save()

    return redirect(reverse("product_detail", kwargs={"slug": slug}))


@login_required
def cart(request):
    # get user cart
    get_cart = Cart.objects.get(user=request.user)

    cart_articles = CartProduct.objects.filter(user_cart=get_cart)

    # save the current products in cart to display them
    products = []

    # initialize a value to calculate the total before shipment fees
    total = 0
    # loop through the cart
    for i in cart_articles:
        # Get the product to access its value price
        get_product = Product.objects.get(id=i.product_id)
        get_product.quantity = i.quantity
        print(get_product.quantity)
        products.append(get_product)
        # Calculate the price based on quantity and price
        total += get_product.price * i.quantity

    # set the total price on the database
    # cart_articles.price = total
    # cart_articles.save()

    return render(request, 'store/cart.html',
                  context={"cart_articles": products, "quantities": cart_articles, "total": total})


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
        # get selected address and carrier from the form
        address_name = request.POST.get("flexAddress")
        carrier_name = request.POST.get("flexCarrier")
        print(carrier_name)

        # set carrier and delivery address
        cart = Cart.objects.get(user=request.user)
        carrier = Delivery.objects.get(id=carrier_name)
        print(address_name)
        cart.address = address_name
        cart.carrier = carrier.id
        cart.save()

        # update total price

        # redirect to the payment page
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

                # get the card
                create_order(request.user)

                return HttpResponseRedirect('/payment/successful')
            else:
                error = True
                return render(request, 'store/payment.html', {'form': form, 'error': error})
    # if the request is a get
    else:
        # load the form created in forms.py
        form = PaymentForm()
        return render(request, 'store/payment.html', {'form': form})


def create_order(user):
    # create a new order
    cart = Cart.objects.get(user=user)
    cart_products = CartProduct.objects.filter(user_cart=cart)
    print(cart)

    #AJOUTER l'user à l'order
    order = Order(order=cart, price=10, user=user)
    order.save()
    order_details = OrderDetails(address=cart.address, carrier=cart.carrier, order=order, total=100)
    order_details.save()

    for i in cart_products:
        get_product = Product.objects.get(id=i.product_id)
        add_product_order = OrderProduct(product=get_product, order_id=order, quantity=i.quantity)
        add_product_order.save()

    # order_details = OrderDetails(address=, carrier=, order=order.id, total=)

    # empty the cart


def payment_successful(request):
    return render(request, 'store/payment_successful.html')


def handle_not_found(request, exception):
    return render(request, 'error/404.html')
