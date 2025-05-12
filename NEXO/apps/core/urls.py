from django.urls import path
from .views import Home

urlpatterns = [
    path('', Home.as_view(), name='home'),
    # La vista de cambio de idioma ahora está definida en config/urls.py
]