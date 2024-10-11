from django.urls import path

import shop.admin_app.views as admin_app
app_name = 'admin_app'

urlpatterns = [
    path('', admin_app.main_admin_page, name='index'),
    path('users/create/', admin_app.UserCreateView.as_view(), name='user_create'),
    path('users/read/', admin_app.UserListView.as_view(), name='users'),
    path('users/update/<int:pk>/', admin_app.UserUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', admin_app.UserDeleteView.as_view(), name='user_delete'),
    path('categories/create/', admin_app.CategoryCreateView.as_view(), name='category_create'),
    path('categories/read/', admin_app.CategoryListView.as_view(), name='categories'),
    path('categories/update/<int:pk>/', admin_app.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', admin_app.CategoryDeleteView.as_view(), name='category_delete'),
    path('products/create/', admin_app.ProductCreateView.as_view(), name='product_create'),
    path('products/read/', admin_app.ProductListView.as_view(), name='products'),
    path('products/read/category/<int:category_pk>/', admin_app.ProductListView.as_view(), name='products_by_category'),
    path('products/read/<int:pk>/', admin_app.ProductDetailView.as_view(), name='product_read'),
    path('products/update/<int:pk>/', admin_app.ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', admin_app.ProductDeleteView.as_view(), name='product_delete'),
]
