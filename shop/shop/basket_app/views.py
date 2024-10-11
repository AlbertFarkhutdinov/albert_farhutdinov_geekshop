from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, HttpResponse
from shop.basket_app.models import BasketSlot
from django.contrib.auth.decorators import login_required
from shop.main_app.models import Product
from django.urls import reverse
from shop.main_app.common_context import page_name
from django.db.models import F
# from django.conf import settings
# from django.core.cache import cache


@login_required
def read(request):
    context = {}
    page_name(context, 'Basket')
    return render(request, 'basket_app/basket.html', context)


@login_required
def add(request, product_pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products_urls:product', args=[product_pk]))
    product = get_object_or_404(Product, pk=product_pk)
    basket_slot = BasketSlot.objects.filter(user=request.user, product=product)
    if basket_slot:
        basket_slot = basket_slot.select_related().first()
    if not basket_slot:
        basket_slot = BasketSlot(user=request.user, product=product)
    else:
        basket_slot.quantity = F('quantity') + 1
    if basket_slot.quantity <= product.quantity:
        basket_slot.save()
    else:
        print('This item is not in stock.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    basket_slot = BasketSlot.objects.filter(user=request.user, product=product)
    if basket_slot:
        basket_slot = basket_slot.select_related().first()
    if basket_slot:
        if basket_slot.quantity > 1:
            basket_slot.quantity = F('quantity') - 1
            basket_slot.save()
        else:
            basket_slot.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit(request, pk):
    if request.is_ajax():
        basket_slot = get_object_or_404(BasketSlot, pk=pk)
        quantity = int(request.GET.get('quantity'))
        if quantity > 0:
            basket_slot.quantity = quantity
            basket_slot.save()
        else:
            basket_slot.delete()
        return HttpResponse('Ok!')


# # Начало кэша
# def get_basket_slot(user, product_pk):
#     product = get_object_or_404(Product, pk=product_pk)
#     if settings.LOW_CACHE:
#         key = f'basket_slot_{user.username}_{product_pk}'
#         cache_basket = cache.get(key)
#         if cache_basket is None:
#             cache_basket = BasketSlot.objects.select_related().filter(user, product).first()
#             cache.set(key, cache_basket)
#         return cache_basket
#     else:
#         return BasketSlot.objects.select_related().filter(user, product).first()
