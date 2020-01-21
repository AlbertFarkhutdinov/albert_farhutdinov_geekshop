from django.contrib import admin
from authapp.models import ShopUser
from basketapp.models import BasketSlot

admin.site.register(ShopUser)


class BasketSlotInline(admin.TabularInline):
    model = BasketSlot
    extra = 0


class ShopUserWithBasket(ShopUser):
    class Meta:
        verbose_name = 'Пользователь с корзиной'
        verbose_name_plural = 'Пользователи с корзиной'
        proxy = True


@admin.register(ShopUserWithBasket)
class ShopUserWithBasketAdmin(admin.ModelAdmin):
    list_display = 'username', 'get_basket_quantity', 'get_basket_cost',
    fields = 'username',
    readonly_fields = 'username',
    inlines = BasketSlotInline,

    def get_queryset(self, request):
        return ShopUser.objects.filter(basket__quantity__gt=0).distinct()

    def get_basket_quantity(self, instance):
        basket = instance.basket.all()
        return sum(list(map(lambda basket_slot: basket_slot.quantity, basket)))

    get_basket_quantity.short_description = 'Товаров в корзине'

    def get_basket_cost(self, instance):
        basket = BasketSlot.objects.filter(user=instance)
        return sum(list(map(lambda basket_slot: basket_slot.cost, basket)))

    get_basket_cost.short_description = 'Стоимость корзины'
