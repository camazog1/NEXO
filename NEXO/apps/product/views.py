from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductImage
from .forms import ProductForm


def product_index(request):
    products = Product.objects.all()
    return render(request, 'product/product_index.html', {'products': products})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            for file in request.FILES.getlist('images'):
                ProductImage.objects.create(product=product, image=file)
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'product/product_form.html', {'form': form})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product/product_detail.html', {'product': product})