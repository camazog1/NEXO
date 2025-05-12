from django.urls import path
from .views import Home
from . import views

urlpatterns = [
    path('', Home.as_view(), name='home'),
    # La vista de cambio de idioma ahora está definida en config/urls.py
    path('productos-aliados/', views.productos_aliados, name='productos_aliados'),
]