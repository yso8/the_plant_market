from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from store.models import Product, Cart, Order, Delivery, Category
from account.models import Address
from django.http import HttpResponseRedirect


def index(request):
    products = Product.objects.all()
    nb_products = len(products)
    return render(request, 'store/index.html', context={"products": products, "nb_products": nb_products})


def filter_products(request, filter):
    products_filter = Product.objects.filter(category=filter)
    filters = Category.objects.all()
    return render(request, 'store/index.html', context={"products": products_filter, "filters": filters})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', context={"product": product})


def check_is_user_logged(request):
    user = request.user
    if user:
        return True


def add_to_cart(request, slug):
    if request.user.is_authenticated:
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

    else:
        return redirect('/login')


def index_add_to_cart(request, slug):
    if request.user.is_authenticated:
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

    else:
        return redirect('/login')


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


def add_to_favorite(request, id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=id)
        print(product)
        # get le produit

        # check if already in fav

        return redirect('index')

    else:
        return redirect('/login')


def delete_cart(request):
    if cart := get_object_or_404(Cart, user=request.user):
        cart.orders.all().delete()
        cart.delete()
    return redirect('index')


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


def select_delivery_method(request):
    addresses = Address.objects.filter(user=request.user)
    deliveries = Delivery.objects.all()
    return render(request, 'store/address_delivery_selector.html', context={"addresses": addresses,
                                                                            "deliveries": deliveries})


def payment_method(request):
    return render(request, 'store/payment.html')
