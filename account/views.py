from django.contrib.auth import get_user_model, login, logout, authenticate
from django.shortcuts import render, redirect
from django.views import generic
from .models import Address, Shopper
from .forms import AddressForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == "POST":
        # get all the fields from the form
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # check if the username and email are already in use
        check_username = Shopper.objects.filter(username=username)
        check_email = Shopper.objects.filter(email=email)
        print(check_email)

        if not check_username and not check_email:
            user = Shopper.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('index')
        # if username already in use
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
        if user:
            login(request, user)
            return redirect('index')
        else:
            error = True
            return render(request, 'account/login.html', context={"error": error})

    return render(request, 'account/login.html')


def logout_user(request):
    logout(request)
    return redirect('index')


@login_required
def account_home(request):
    return render(request, 'account/user_settings.html')


@login_required
def account_address(request):
    # fetchs les adresses du user
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'account/user_address.html', context={"addresses": addresses})


@login_required
def account_address_add(request):
    if request.method == 'POST':
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
                error = True
                return render(request, 'account/user_add_address.html', {'form': form, 'error': error})
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
    return render(request, 'account/user_orders.html')


@login_required
def account_return(request):
    return render(request, 'account/user_return.html')
