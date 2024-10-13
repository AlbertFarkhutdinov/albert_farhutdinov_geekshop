from django.urls import path

import shop.orders_app.views as orders_app

app_name = 'orders_app'

urlpatterns = [
    path('', orders_app.OrderList.as_view(), name='orders_list'),
    path(
        'forming/complete/<int:pk>/',
        orders_app.order_forming_complete,
        name='order_forming_complete',
    ),
    path(
        'create/',
        orders_app.OrderItemsCreate.as_view(),
        name='order_create',
    ),
    path(
        'read/<int:pk>/',
        orders_app.OrderRead.as_view(),
        name='order_read',
    ),
    path(
        'update/<int:pk>/',
        orders_app.OrderItemsUpdate.as_view(),
        name='order_update',
    ),
    path(
        'delete/<int:pk>/',
        orders_app.OrderDelete.as_view(),
        name='order_delete',
    ),
    path('product/<int:pk>/price/', orders_app.get_product_price),
]
