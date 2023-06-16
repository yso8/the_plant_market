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

    if request.user.is_authenticated:
        favorites = request.user.favorite.all()
        return render(request, 'store/index.html', context={"products": products, "filters": filters, "favorites": favorites})

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

    if request.user.is_authenticated:
        is_favorite = False
        for i in request.user.favorite.all():
            if i == product:
                is_favorite = True
                
        return render(request, 'store/product_detail.html', context={"product": product, "is_favorite": is_favorite})
    
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
            if product.quantity - 1 >= 0:
                add_article = CartProduct(product=product, quantity=1, user_cart=get_cart)
                add_article.save()
            else:
                return render(request, 'store/index.html', {'error': True})

        # if product is already in the cart, add one to the quantity
        if get_product_cart:
            if product.quantity - 1 >= 0:
                get_product_cart.quantity += 1
                get_product_cart.save()
            else:
                return render(request, 'store/index.html', {'error': True})

    except Cart.DoesNotExist:
        create_cart = Cart(user=request.user)
        create_cart.save()
        if product.quantity - 1 >= 0:
            add_article = CartProduct(product=product, quantity=1, user_cart=create_cart)
            add_article.save()
        else:
            return render(request, 'store/index.html', {'error': True})

    return redirect(reverse("product_detail", kwargs={"slug": slug}))


@login_required
def cart(request):
    # get products in the user cart
    cart_articles = Cart.getUserCartAndProducts(request.user)

    # initialize the total cost of the cart before shipping fees
    total = Cart.getTotalCartPrice(request.user)

    # Count the number of products in the cart
    number_of_products = Cart.getProductsLength(cart_articles)

    if request.method == "POST":
        # List used to store all the products where quantity asked is bigger than available
        errors = []
        for article in cart_articles:
            # if some quantities are equal or inferior to 0, returns error and update quantity in cart
            available_quantity = Product.objects.get(id=article.product.id).quantity
            if article.quantity > available_quantity > 0:
                article.quantity = available_quantity
                article.save()
                error_msg = f'The quantity asked for {article.product.name} is bigger than left: {available_quantity}'
                errors.append(error_msg)
            # If no items are left
            elif available_quantity == 0:
                article.delete()

        # If all the quantity asked are available
        if not errors:
            return redirect('/cart/delivery')
        else:
            errors.append('Quantities have been automatically updated or remove to match those available')
            return render(request, 'store/cart.html',
                          context={"cart_articles": cart_articles, "total": total,
                                   "products_number": number_of_products, 'errors': errors})
    
    return render(request, 'store/cart.html',
                  context={"cart_articles": cart_articles, "total": total,
                           "products_number": number_of_products})

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
def remove_to_favorite(request, id):
    # get the product selected by user
    product = Product.objects.get(id=id)

    # get the current user
    user = Shopper.objects.get(id=request.user.id)
    user.favorite.remove(product)

    return redirect('index')

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
    # if we still need his information
    addresses = Address.objects.filter(user=request.user)
    deliveries = Delivery.objects.all()

    if request.method == 'POST':
        if request.POST.get("flexAddress") and request.POST.get("flexCarrier"):
            # get selected address and carrier from the form
            address_name = request.POST.get("flexAddress")
            carrier_name = request.POST.get("flexCarrier")

            # set carrier and delivery address
            cart = Cart.objects.get(user=request.user)
            carrier = Delivery.objects.get(id=carrier_name)
            cart.address = address_name
            cart.carrier = carrier.id
            cart.save()

            # redirect to the payment page
            return HttpResponseRedirect('/payment')
        else:
            return render(request, 'store/address_delivery_selector.html', {'addresses': addresses,
                                                                            'deliveries': deliveries,
                                                                            'error': True})

    return render(request, 'store/address_delivery_selector.html', context={"addresses": addresses,
                                                                            "deliveries": deliveries})


@login_required
def payment_method(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            response = False
            holderName = form.cleaned_data['name']
            cardNumber = form.cleaned_data['card_number']
            expirationDate = form.cleaned_data['expiration_date']
            CVV = form.cleaned_data['cvv']
            print(holderName)
            print(cardNumber)
            print(expirationDate)
            print(CVV)
            
            # get the cart
            if holderName == "John Toe" and cardNumber == '123456789' and expirationDate == "07/23" and CVV == "123":
                response = True

            # If entered information are correct, create the order and return to the successful page
            if response:
                create_order(request.user)
                return render(request, 'store/payment_successful.html')
            else:
                return render(request, 'store/payment.html', {'form': form, 'error': True})

    # Load the form created in forms.py
    form = PaymentForm()
    return render(request, 'store/payment.html', {'form': form})


def cart_checker(holderName, cardNumber, expirationDate, CVV):
    return_val = False
    if holderName == "Jon Doe" and cardNumber == "123456789" and expirationDate == "07/23" and CVV == 123:
        print('Là')
        return_val = True
    return return_val


def create_order(user):
    # create a new order
    print(user)
    cart = Cart.objects.get(user=user)
    cart_products = CartProduct.objects.filter(user_cart=cart)

    # get the total price
    total = 0
    for product in cart_products:
        total += product.product.price * product.quantity

    order = Order(order=cart, price=total, user=user)
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
    print("Dans test ajax")
    jsonData = json.loads(request.body)
    dataReceived = jsonData.get('selectedProduct')
    return JsonResponse({"Donnée bien reçue": dataReceived})
