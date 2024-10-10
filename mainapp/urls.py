from django.urls import path
import mainapp.views as mainapp
from django.views.decorators.cache import cache_page

app_name = 'mainapp'
urlpatterns = [
    path('', mainapp.main, name='featured'),
    path('new', mainapp.main, name='new'),
    path('hot', mainapp.products, name='hot'),
    path('product/<int:pk>/', mainapp.product, name='product'),
    path('category/<int:pk>/', mainapp.products, name='category'),
    # path('category/<int:pk>/ajax/', cache_page(3600)(mainapp.products_ajax), name='category'),
]
