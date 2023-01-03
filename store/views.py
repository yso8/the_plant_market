from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from store.models import Product, Cart, Order, Delivery, Category, CartProduct, OrderDetails, OrderProduct
from account.models import Shopper
from account.models import Address
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import PaymentForm
import json


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
    print(product.id)

    try:
        get_cart = Cart.objects.get(user=request.user)

        get_product_cart = ""

        try:
            get_product_cart = CartProduct.objects.get(product=product)
        except CartProduct.DoesNotExist:
            add_article = CartProduct(product=product, quantity=1, user_cart=get_cart)
            add_article.save()

        # if product is already in the cart, add one to the quantity
        if get_product_cart:
            get_product_cart.quantity += 1
            get_product_cart.save()

    except Cart.DoesNotExist:
        create_cart = Cart(user=request.user)
        create_cart.save()
        add_product = CartProduct(product=product, quantity=1, user_cart=create_cart)
        add_product.save()

    return redirect(reverse("product_detail", kwargs={"slug": slug}))


@login_required
def cart(request):
    if request.method == "POST":
        print("Dans le post du cart")

        # if some quantities are equal or inferior to 0, returns error

        # else go to payment

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
        products.append(get_product)
        # Calculate the price based on quantity and price
        total += get_product.price * i.quantity

    return render(request, 'store/cart.html',
                  context={"cart_articles": products, "quantities": cart_articles, "total": total,
                           "products_number": len(products)})


def quantity_check():
    print("Update quantity")


@login_required
def add_to_favorite(request, id):
    # get the product selected by user
    product = Product.objects.get(id=id)

    # get the current user
    user = Shopper.objects.get(id=request.user.id)
    user.favorite.add(product)

    return redirect('index')

    # check if product is already in favorite


@login_required
def show_favorite(request):
    # load all the favorites from the logged user
    user = Shopper.objects.get(id=request.user.id)

    favorites = []

    # loop through user favorites
    for favorite in user.favorite.all():
        favorites.append(favorite)

    return render(request, 'store/favorite.html', context={"favorites": favorites})


@login_required
def delete_cart(request):
    if cart := get_object_or_404(Cart, user=request.user):
        cart.orders.all().delete()
        cart.delete()
    return redirect('index')


@login_required
def delete_product_to_cart(request, slug):
    product = Product.objects.get(slug=slug)
    get_cart = Cart.objects.get(user_id=request.user.id)
    cart_products = CartProduct.objects.get(user_cart=get_cart, product_id=product.id)
    cart_products.delete()

    return redirect('/cart')


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
    # load the form created in forms.py
    form = PaymentForm()
    return render(request, 'store/payment.html', {'form': form})


def payment_check(request):
    holder = request.POST.get("card_holder")
    number = request.POST.get("card_number")
    expiration = request.POST.get("expiration_date")
    cvv = request.POST.get("cvv")

    controller_response = ""

    if holder and number and expiration and cvv:
        result_check = cart_checker(holder, number, expiration, cvv)
        if result_check:
            controller_response = {"data": "success"}
    else:
        controller_response = {"data": "error"}

    return JsonResponse(controller_response)


def cart_checker(holder, number, expiration, cvv):
    return_val = False
    if holder == 'Admin admin' and number == '1234567812345678' and expiration == '01/23' and cvv == 123:
        return_val = True
    print(return_val)
    return return_val


def create_order(user):
    # create a new order
    cart = Cart.objects.get(user=user)
    cart_products = CartProduct.objects.filter(user_cart=cart)

    order = Order(order=cart, price=10, user=user)
    order.save()
    print(order.order_id)
    order_details = OrderDetails(address=cart.address, carrier=cart.carrier, order=order, total=100)
    order_details.save()

    for i in cart_products:
        product = Product.objects.get(id=i.product_id)
        add_product_order = OrderProduct(product=product, order_id=order, quantity=i.quantity)
        add_product_order.save()
        update_products_quantity(product, i.quantity)

    empty_cart(cart)


def update_products_quantity(product, quantity):
    product.quantity -= quantity
    product.save()


def empty_cart(cart):
    # empty the cart after the order has been completed
    Cart(id=cart.id).delete()


def payment_successful(request):
    return render(request, 'store/payment_successful.html')


def handle_not_found(request, exception):
    return render(request, 'error/404.html')

@login_required
def test_ajax(request):
    print("Dans tets ajax")
    jsonData = json.loads(request.body)
    dataReceived = jsonData.get('selectedProduct')
    return JsonResponse({"Donnée bien reçue": dataReceived})
