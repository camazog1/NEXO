from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductImage
from .forms import ProductForm
from django.db.models import Q

def product_index(request):
    query = request.GET.get('q') 
    if query:
        products = Product.objects.filter(Q(title__icontains=query)| Q(description__icontains=query))
    else:
        products = Product.objects.all()
    return render(request, 'product/product_index.html', {'products': products, 'query': query})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product/product_detail.html', {'product': product})