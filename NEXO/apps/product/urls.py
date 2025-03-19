from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.product_index, name='product_index'),
    path('<str:pk>/', views.product_detail, name='product_detail'),
]
