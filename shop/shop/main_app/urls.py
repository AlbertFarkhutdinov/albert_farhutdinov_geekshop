from django.urls import path
import main_app.views as main_app
from django.views.decorators.cache import cache_page

app_name = 'main_app'
urlpatterns = [
    path('', main_app.main, name='featured'),
    path('new', main_app.main, name='new'),
    path('hot', main_app.products, name='hot'),
    path('product/<int:pk>/', main_app.product, name='product'),
    path('category/<int:pk>/', main_app.products, name='category'),
    # path('category/<int:pk>/ajax/', cache_page(3600)(main_app.products_ajax), name='category'),
]
