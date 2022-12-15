from django.contrib.auth import get_user_model, login, logout, authenticate
from django.shortcuts import render, redirect
from django.views import generic

User = get_user_model()


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('index')

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


def my_account(request):
    return render(request, 'account/signup.html')


def account_home(request):
    return render(request, 'account/user_settings.html')


def account_address(request):
    return render(request, 'account/user_address.html')


def account_order(request):
    return render(request, 'account/user_orders.html')


def account_return(request):
    return render(request, 'account/user_return.html')


def add_new_adress(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('index')
