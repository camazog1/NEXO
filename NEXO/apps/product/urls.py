from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.product_index, name='product_index'),
    path('create/', views.product_create, name='product_create'),
    path('<str:pk>/', views.product_detail, name='product_detail'),
    path('reports/<str:format_type>/', views.generate_product_report, name='generate_product_report'),
]
