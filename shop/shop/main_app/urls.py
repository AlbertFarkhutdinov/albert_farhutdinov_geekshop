from django.urls import path

from shop.main_app import views as main_app_views

# from django.views.decorators.cache import cache_page


app_name = 'main_app'
urlpatterns = [
    path('', main_app_views.main, name='featured'),
    path('new', main_app_views.main, name='new'),
    path('hot', main_app_views.products, name='hot'),
    path('product/<int:pk>/', main_app_views.product, name='product'),
    path('category/<int:pk>/', main_app_views.products, name='category'),
    # path(
    #     'category/<int:pk>/ajax/',
    #     cache_page(3600)(main_app.products_ajax),
    #     name='category',
    # ),
]
