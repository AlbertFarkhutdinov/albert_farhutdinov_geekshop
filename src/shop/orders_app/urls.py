from django.urls import path

from shop.orders_app import views as orders_app_views

app_name = 'orders_app'

urlpatterns = [
    path('', orders_app_views.OrderList.as_view(), name='orders_list'),
    path(
        'forming/complete/<int:pk>/',
        orders_app_views.order_forming_complete,
        name='order_forming_complete',
    ),
    path(
        'create/',
        orders_app_views.OrderItemsCreate.as_view(),
        name='order_create',
    ),
    path(
        'read/<int:pk>/',
        orders_app_views.OrderRead.as_view(),
        name='order_read',
    ),
    path(
        'update/<int:pk>/',
        orders_app_views.OrderItemsUpdate.as_view(),
        name='order_update',
    ),
    path(
        'delete/<int:pk>/',
        orders_app_views.OrderDelete.as_view(),
        name='order_delete',
    ),
    path('product/<int:pk>/price/', orders_app_views.get_product_price),
]
