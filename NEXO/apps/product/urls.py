from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('index/', views.product_index, name='product_index'),
    path('create/', views.product_create, name='product_create'),
    path('<str:pk>/', views.product_detail, name='product_detail'),
    path('reports/<str:format_type>/', views.generate_product_report, name='generate_product_report'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
