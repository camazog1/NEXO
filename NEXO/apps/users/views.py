from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

SUPERADMIN_PASSWORD = "superadmin_secret" 

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        user_type = request.POST['user_type']

        if user_type == 'admin':
            superadmin_password = request.POST.get('superadmin_password')
            if superadmin_password != SUPERADMIN_PASSWORD:
                messages.error(request, _('The special admin password is incorrect.'))
                return render(request, 'users/signup.html')

        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type
        )
        login(request, user)
        return redirect('home')  

    return render(request, 'users/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_index')
        else:
            messages.error(request, _('Invalid credentials'))
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')