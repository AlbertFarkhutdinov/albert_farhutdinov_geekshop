from django.urls import path

from shop.auth_app import views as auth_app_views

app_name = 'auth_app'

urlpatterns = [
    path('register/', auth_app_views.register, name='register'),
    path('login/', auth_app_views.login, name='login'),
    # path('edit/<int:pk>/', auth_app_views.EditView.as_view(), name='edit'),
    path('edit/<int:pk>/', auth_app_views.edit, name='edit'),
    path('logout/', auth_app_views.logout, name='logout'),
    path(
        'verify/<str:email>/<str:activation_key>/',
        auth_app_views.verify,
        name='verify',
    ),
]
