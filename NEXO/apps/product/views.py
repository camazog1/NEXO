from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductImage
from .forms import ProductForm
from django.db.models import Q

def product_index(request):
    # 1. Capturar el término de búsqueda (query)
    query = request.GET.get('q')
    
    # 2. Capturar el criterio de orden (sort)
    sort = request.GET.get('sort')
    
    # 3. Filtrar por búsqueda
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()
    
    # 4. Ordenar según el parámetro 'sort'
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'alpha':
        products = products.order_by('title')
    # Si no hay sort, se deja el orden por defecto

    return render(request, 'product/product_index.html', {
        'products': products,
        'query': query,  # para mostrar el valor en el template si quieres
    })

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