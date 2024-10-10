from django.urls import path
from basketapp.views import add, remove, read, edit

app_name = 'basketapp'

urlpatterns = [
    path('add/<int:product_pk>/', add, name='add'),
    path('remove/<int:product_pk>/', remove, name='remove'),
    path('', read, name='read'),
    path('edit/<int:pk>/', edit, name='edit'),
]
