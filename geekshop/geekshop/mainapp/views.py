from django.shortcuts import render, get_object_or_404
from mainapp.models import Product, ProductCategory
from mainapp.common_context import page_name
from django.conf import settings
from django.core.cache import cache
# from django.template.loader import render_to_string
# from django.views.decorators.cache import cache_page
# from django.http import JsonResponse


# Контроллеры
def main(request):
    all_products = get_products()
    keys = [item.pk for item in all_products]
    context = {'products': all_products,
               'new_products': all_products.filter(is_new=True),
               'featured_products': all_products.filter(is_featured=True),
               'hot_products': all_products.filter(is_hot=True),
               'trending_products': all_products.filter(pk__lte=min(keys) + 5)
               }
    page_name(context, 'Home page')
    return render(request, 'mainapp/index.html', context)


def products(request, pk=None):
    product_categories = get_categories()
    all_products = get_products().order_by('price')
    if pk is None:
        context = {'product_categories': product_categories,
                   'hot_product': all_products.filter(is_hot=True).first(),
                   }
        page_name(context, 'Hot Deal')
        return render(request, 'mainapp/hot_product.html', context)
    else:
        if pk > 0:
            all_products = get_products_in_category(pk).order_by('price')
        context = {'product_categories': product_categories,
                   'products': all_products,
                   }
        page_name(context, 'Our Product Range')
        return render(request, 'mainapp/products.html', context)


def history(request):
    context = {}
    page_name(context, 'History')
    return render(request, 'mainapp/history.html', context)


def showroom(request):
    context = {}
    page_name(context, 'Showroom')
    return render(request, 'mainapp/showroom.html', context)


def contacts(request):
    context = {}
    page_name(context, 'Contact Us')
    return render(request, 'mainapp/contacts.html', context)


def product(request, pk):
    current_product = get_product(pk)
    product_categories = get_categories()
    context = {
        'product_categories': product_categories,
        'product': current_product,
    }
    page_name(context, current_product.name)
    return render(request, 'mainapp/product.html', context)


# Начало кэша
def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        cache_products = cache.get(key)
        if cache_products is None:
            cache_products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, cache_products)
        return cache_products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_categories():
    if settings.LOW_CACHE:
        key = 'categories'
        cache_categories = cache.get(key)
        if cache_categories is None:
            cache_categories = ProductCategory.objects.filter(is_active=True)
            cache.set(key, cache_categories)
        return cache_categories
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_products_in_category(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_{pk}'
        cache_products = cache.get(key)
        if cache_products is None:
            cache_products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True)
            cache.set(key, cache_products)
        return cache_products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True)


def get_cache_object(model, key_word, pk):
    if settings.LOW_CACHE:
        key = f'{key_word}_{pk}'
        cache_object = cache.get(key)
        if cache_object is None:
            cache_object = get_object_or_404(model, pk=pk)
            cache.set(key, cache_object)
            return cache_object
        else:
            return get_object_or_404(model, pk=pk)


def get_category(pk):
    return get_cache_object(model=ProductCategory, key_word='category', pk=pk)


def get_product(pk):
    return get_cache_object(model=Product, key_word='product', pk=pk)


# # AJAX
# def products_ajax(request, pk=None):
#     if request.is_ajax():
#         product_categories = get_links_menu()
#         if pk:
#             if pk == '0':
#                 _category = {
#                     'pk': 0,
#                     'name': 'ALL'
#                 }
#                 _products = get_products(ordered_by_price=True)
#             else:
#                 _category = get_category(pk)
#                 _products = get_products_in_category_ordered_by_price(pk)
#             content = {
#                 'product_categories': product_categories,
#                 'category': _category,
#             }
#             result = render_to_string('mainapp/includes/inc_products_sheet.html', context=content, request=request)
#             return JsonResponse({'result': result})
