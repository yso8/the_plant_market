from django.contrib.auth import get_user_model, login, logout, authenticate
from django.shortcuts import render, redirect
from django.views import generic
from .models import Address, Shopper
from store.models import Order, OrderProduct, Product
from .forms import AddressForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == "POST":
        # get all the fields from the form
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confpassword")
        print(confirm_password)

        # check if the username and email are already in use
        check_username = Shopper.objects.filter(username=username)
        check_email = Shopper.objects.filter(email=email)

        if not check_username and not check_email and password == confirm_password:
            user = Shopper.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('index')
        # if username already in use
        elif password != confirm_password:
            error_password = True
            return render(request, 'account/signup.html',
                          {"error_password": error_password})
        elif check_username and check_email:
            error_username = True
            error_email = True
            return render(request, 'account/signup.html',
                          {"error_username": error_username, "error_email": error_email})
        # if email already in use
        elif check_email:
            error_email = True
            return render(request, 'account/signup.html', {"error_email": error_email})
        else:
            error_username = True
            return render(request, 'account/signup.html', {"error_username": error_username})

    else:
        return render(request, 'account/signup.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        # if user is successfully authenticated, send him on the index page
        if user:
            login(request, user)
            return redirect('index')
        # throw an error in the template saying its credentials are incorrect
        else:
            error = True
            return render(request, 'account/login.html', context={"error": error})

    return render(request, 'account/login.html')


def logout_user(request):
    logout(request)
    return redirect('index')


@login_required
def account_home(request):
    # returns base page for user account
    return render(request, 'account/user_settings.html')


@login_required
def account_address(request):
    # get the address for the current user
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'account/user_address.html', context={"addresses": addresses})


@login_required
def account_address_add(request):
    if request.method == 'POST':
        print("dans le post")
        form = AddressForm(request.POST)
        if form.is_valid():
            # create new address
            name = form.cleaned_data['name']
            city = form.cleaned_data['city']
            postal_code = form.cleaned_data['postal_code']
            address_complement = form.cleaned_data['address_complement']
            # check if address name already exists or not
            address = Address.objects.filter(name=name, user=request.user)

            if address:
                error_address = True
                return render(request, 'account/user_add_address.html', {'form': form, 'error_address': error_address})

            if postal_code != 5:
                postal_error = True
                return render(request, 'account/user_add_address.html', {'form': form, 'error_postal': postal_error})
            else:
                address = Address(name=name, city=city,
                                  postal_code=postal_code, address_complement=address_complement, user=request.user)
                address.save()
                return HttpResponseRedirect('/account/addresses')
    else:
        form = AddressForm()

    return render(request, 'account/user_add_address.html', {'form': form})


@login_required
def account_address_update(request, id):
    if request.method == 'POST':
        form = AddressForm(request.PUT)
        if form.is_valid():
            # create new address
            name = form.cleaned_data['name']
            city = form.cleaned_data['city']
            postal_code = form.cleaned_data['postal_code']
            address_complement = form.cleaned_data['address_complement']
            # check if address name already exists or not
            address = Address.objects.filter(name=name, user=request.user)
            if address:
                error = True
                return render(request, 'account/user_update_address.html', {'form': form, 'error': error})
            else:
                address = Address(name=name, city=city,
                                  postal_code=postal_code, address_complement=address_complement, user=request.user)
                address.save()
                return HttpResponseRedirect('/account/addresses')
    else:
        # get the current data of the selected address
        address = Address.objects.filter(id=id, user=request.user).first()
        form = AddressForm(initial={'name': address.name, 'city': address.city, 'postal_code': address.postal_code,
                                    'address_complement:': address.address_complement})
        return render(request, 'account/user_update_address.html', {'form': form})


@login_required
def account_address_delete(request, id):
    Address.objects.filter(id=id, user=request.user).delete()
    return HttpResponseRedirect('/account/addresses')


@login_required
def account_order(request):
    get_orders = Order.objects.filter(user_id=request.user)

    return render(request, 'account/user_orders.html', {"orders": get_orders})


@login_required
def order_details(request, id):
    # Get the order by its id and user connected to make sure to fetch only its orders
    order = Order.objects.get(user=request.user, id=id)
    ordered_products = OrderProduct.objects.filter(order_id=order)

    return render(request, 'account/user_order_details.html', {"products": ordered_products})


@login_required
def account_return(request):
    return render(request, 'account/user_return.html')
