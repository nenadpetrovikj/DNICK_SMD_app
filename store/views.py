from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render, redirect

from .models import Category, Product
from .forms import AddProductForm


def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            user = request.user
            product.created_by = user
            product.save()
            return redirect(product.category.get_absolute_url())
    else:
        form = AddProductForm()
    
    return render(request, 'store/add-product.html', {'form': form})

def home(request):
    return render(request, 'store/home.html')

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)

    context = {
        'product': product
    }

    return render(request, 'store/products/detail.html', context)

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.products.filter(category=category)
    
    unique_brands = set()
    unique_screens = set()
    unique_battery_sizes = set()
    unique_processors = set()
    unique_oses = set()
    min_price = float('inf')
    max_price = float('-inf')
    
    for product in products:
        unique_brands.add(product.manufacturer)
        unique_screens.add(product.screen)
        unique_battery_sizes.add(product.battery)
        unique_processors.add(product.processor)
        unique_oses.add(product.os)
        price = product.price
        if price < min_price:
            min_price = price
        if price > max_price:
            max_price = price


    context = {
        'category': category,
        'products': products,
        'brands': list(unique_brands),
        'screens': list(unique_screens),
        'battery_sizes': list(unique_battery_sizes),
        'processors': list(unique_processors),
        'oses': list(unique_oses),
        'min_price': min_price,
        'max_price': max_price,
    }

    return render(request, 'store/products/category.html', context)


