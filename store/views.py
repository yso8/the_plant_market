from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from store.models import Product, Cart, Order


def index(request):
    products = Product.objects.filter()
    nb_products = len(products)
    return render(request, 'store/index.html', context={"products":products, "nb_products":nb_products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', context={"product":product})


def add_to_cart(request, slug):
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

    return redirect(reverse("product_detail", kwargs={"slug":slug}))


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

    return redirect('index')


def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'store/cart.html', context={"orders":cart.orders.all()})


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
