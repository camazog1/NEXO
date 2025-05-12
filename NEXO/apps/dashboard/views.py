from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from apps.product.models import Product
from apps.product.forms import ProductForm
from django.utils.translation import gettext_lazy as _

# Create your views here.

def is_admin(user):
    return user.is_authenticated and user.user_type == 'admin'

@login_required
@user_passes_test(is_admin)
def product_list(request):
    products = Product.objects.all()
    return render(request, 'dashboard/dashboard.html', {'products': products})

@login_required
@user_passes_test(is_admin)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _('Product created successfully!'))
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'dashboard/product_create.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, _('Product updated successfully!'))
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/product_update.html', {'form': form, 'product': product})

@login_required
@user_passes_test(is_admin)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, _('Product deleted successfully!'))
        return redirect('product_list')
    return render(request, 'dashboard/product_delete.html', {'product': product})