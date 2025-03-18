from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        # Crear usuario
        user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, last_name=last_name)
        # Iniciar sesión automáticamente después de registrarse (opcional)
        login(request, user)
        return redirect('home')  # Ajusta a la URL que deseas redireccionar

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
            messages.error(request, 'Credenciales inválidas')
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')