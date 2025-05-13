from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('products/', views.product_list, name='product_list'),  # List all products
    path('products/<str:pk>/update/', views.product_update, name='product_update'),  # Update a product
    path('products/<str:pk>/delete/', views.product_delete, name='product_delete'),  # Delete a product
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)