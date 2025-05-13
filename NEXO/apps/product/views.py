from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductImage
from .forms import ProductForm
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, Http404
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Importar las clases de generación de reportes
from .reports.report_factory import ReportFactory

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

@login_required
def generate_product_report(request, format_type):
    if format_type not in ['pdf', 'excel']:
        messages.error(request, _("Formato de reporte no válido. Use 'pdf' o 'excel'."))
        return redirect('product_index')
    
    report_generator = ReportFactory.get_report_generator(format_type)
    
    if not report_generator:
        messages.error(request, _("No se pudo crear el generador de reportes para el formato especificado."))
        return redirect('product_index')
    
    products = Product.objects.all()
    
    products_data = []
    for product in products:
        products_data.append({
            'reference': product.reference,
            'title': product.title,
            'description': product.description,
            'price': product.price,
            'price_dolar': float(product.price_dolar),
            'is_popular': product.is_popular,
            'is_new': product.is_new,
            'discontinued': product.discontinued,
        })
    
    return report_generator.generate_product_report(
        products=products_data,
        title=_("NEXO Products Report")
    )

def api_products(request):
    """
    API endpoint que devuelve todos los productos en formato JSON.
    """
    products = Product.objects.all()
    
    # Crear una lista con la información relevante de cada producto
    products_data = []
    for product in products:
        # Obtener la URL absoluta para el detalle del producto
        product_url = request.build_absolute_uri(
            reverse('product_detail', kwargs={'pk': product.reference})
        )
        
        # Añadir los datos del producto
        products_data.append({
            'title': product.title,
            'reference': product.reference,
            'description': product.description,
            'price': product.price,
            'price_dolar': float(product.price_dolar),
            'is_popular': product.is_popular,
            'is_new': product.is_new,
            'discontinued': product.discontinued,
            'url': product_url,
        })
    
    # Crear la respuesta JSON
    response_data = {
        'products': products_data,
        'count': len(products_data),
        'service_info': {
            'name': 'NEXO Product API',
            'version': '1.0',
            'description': 'API para obtener información de productos NEXO'
        }
    }
    
    # Crear la respuesta con los encabezados CORS apropiados
    response = JsonResponse(response_data)
    response["Access-Control-Allow-Origin"] = "*"  # Permitir solicitudes desde cualquier origen
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    
    return response