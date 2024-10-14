from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.cache import cache
from django.db import transaction
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.detail import DetailView

from shop.basket_app.models import BasketSlot
from shop.main_app.common_context import get_basket, page_name
from shop.main_app.models import Product
from shop.orders_app.forms import OrderItemForm
from shop.orders_app.models import Order, OrderItem


class IsAuthenticatedUser(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated


class OrderList(IsAuthenticatedUser, ListView):
    model = Order

    def get_queryset(self):
        return get_order_list(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(OrderList, self).get_context_data(**kwargs)
        page_name(context, 'Your orders')
        return context


class OrderItemsCreate(IsAuthenticatedUser, CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order_urls:orders_list')

    def get_context_data(self, **kwargs):
        context = super(OrderItemsCreate, self).get_context_data(**kwargs)
        order_form_set = inlineformset_factory(
            parent_model=Order,
            model=OrderItem,
            form=OrderItemForm,
            extra=1,
        )
        if self.request.POST:
            formset = order_form_set(self.request.POST)
        else:
            basket_items = get_basket(self.request.user)
            if len(basket_items):
                order_form_set = inlineformset_factory(
                    parent_model=Order,
                    model=OrderItem,
                    form=OrderItemForm,
                    extra=len(basket_items),
                )
                formset = order_form_set()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                basket_items.delete()
            else:
                formset = order_form_set()
        context['order_items'] = formset
        page_name(context, 'New order')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['order_items']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if order_items.is_valid():
                order_items.instance = self.object
                order_items.save()
        if self.object.get_total_cost() == 0:
            self.object.delete()
        return super(OrderItemsCreate, self).form_valid(form)


class OrderItemsUpdate(IsAuthenticatedUser, UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order_urls:orders_list')

    def get_context_data(self, **kwargs):
        context = super(OrderItemsUpdate, self).get_context_data(**kwargs)
        order_form_set = inlineformset_factory(
            parent_model=Order,
            model=OrderItem,
            form=OrderItemForm,
            extra=1,
        )
        if self.request.POST:
            context['order_items'] = order_form_set(
                self.request.POST,
                instance=self.object,
            )
        else:
            queryset = self.object.order_items.select_related()
            formset = order_form_set(instance=self.object, queryset=queryset)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
            context['order_items'] = formset
        page_name(context, 'Update order')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['order_items']
        with transaction.atomic():
            self.object = form.save()
            if order_items.is_valid():
                order_items.instance = self.object
                order_items.save()
        if self.object.get_summary()['total_cost'] == 0:
            self.object.delete()
        return super(OrderItemsUpdate, self).form_valid(form)


class OrderDelete(IsAuthenticatedUser, DeleteView):
    model = Order
    success_url = reverse_lazy('order_urls:orders_list')


class OrderRead(IsAuthenticatedUser, DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        page_name(context, 'Order/Watch')
        return context


@user_passes_test(lambda user: user.is_authenticated)
def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('order_urls:orders_list'))


@user_passes_test(lambda user: user.is_authenticated)
@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=BasketSlot)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if update_fields in {'quantity', 'product'}:
        if instance.pk and sender.get_item(instance.pk):
            instance.product.quantity -= (
                instance.quantity - sender.get_item(instance.pk).quantity
            )
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()


@user_passes_test(lambda user: user.is_authenticated)
@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=BasketSlot)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()


def get_product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.filter(pk=int(pk)).first()
        if product:
            return JsonResponse({'price': product.price})
        return JsonResponse({'price': 0})
    return None


def get_order_list(user):
    if settings.LOW_CACHE:
        key = 'order_list'
        cache_object = cache.get(key)
        if cache_object is None:
            cache_object = Order.objects.filter(user=user)
            cache.set(key, cache_object)
        return cache_object
    return Order.objects.filter(user=user)
