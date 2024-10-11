from django.urls import path

import auth_app.views as auth_app

app_name = 'auth_app'

urlpatterns = [
    path('register/', auth_app.register, name='register'),
    path('login/', auth_app.login, name='login'),
    # path('edit/<int:pk>/', auth_app.EditView.as_view(), name='edit'),
    path('edit/<int:pk>/', auth_app.edit, name='edit'),
    path('logout/', auth_app.logout, name='logout'),
    path('verify/<str:email>/<str:activation_key>/', auth_app.verify, name='verify'),
]
