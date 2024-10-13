from django.contrib import admin

from shop.auth_app.models import ShopUser
from shop.basket_app.models import BasketSlot

admin.site.register(ShopUser)


class BasketSlotInline(admin.TabularInline):
    model = BasketSlot
    extra = 0


class ShopUserWithBasket(ShopUser):
    class Meta:
        verbose_name = 'User with basket'
        verbose_name_plural = 'Users with basket'
        proxy = True


@admin.register(ShopUserWithBasket)
class ShopUserWithBasketAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_basket_quantity', 'get_basket_cost')
    fields = ('username',)
    readonly_fields = ('username',)
    inlines = (BasketSlotInline,)

    def get_queryset(self, request):
        return ShopUser.objects.filter(basket__quantity__gt=0).distinct()

    def get_basket_quantity(self, instance):
        basket = instance.basket.all()
        return sum([basket_slot.quantity for basket_slot in basket])

    get_basket_quantity.short_description = 'Items in basket'

    def get_basket_cost(self, instance):
        basket = BasketSlot.objects.filter(user=instance)
        return sum([basket_slot.cost for basket_slot in basket])

    get_basket_cost.short_description = 'Basket Cost'
