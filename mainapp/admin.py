from django.contrib import admin
from mainapp.models import ProductCategory, Product

admin.site.register(ProductCategory)
# admin.site.register(Product)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'name', 'category', 'is_hot', 'is_featured', 'is_new'
    list_filter = 'is_hot', 'is_featured', 'is_new'
    search_fields = 'name', 'category__name',
    readonly_fields = 'quantity',
