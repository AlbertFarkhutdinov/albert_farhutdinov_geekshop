from django.contrib import admin

from shop.orders_app.models import Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = 'name', 'category', 'is_hot', 'is_featured', 'is_new'
#     list_filter = 'is_hot', 'is_featured', 'is_new'
#     search_fields = 'name', 'category__name',
#     readonly_fields = 'quantity',
