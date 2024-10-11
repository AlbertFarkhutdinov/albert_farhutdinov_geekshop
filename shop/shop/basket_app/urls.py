from django.urls import path
from shop.basket_app.views import add, remove, read, edit

app_name = 'basket_app'

urlpatterns = [
    path('add/<int:product_pk>/', add, name='add'),
    path('remove/<int:product_pk>/', remove, name='remove'),
    path('', read, name='read'),
    path('edit/<int:pk>/', edit, name='edit'),
]
