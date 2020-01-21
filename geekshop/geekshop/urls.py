"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainapp.views import contacts, history, showroom
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authapp.urls', namespace='auth_urls')),
    path('', include('mainapp.urls', namespace='main_urls')),
    path('products/', include('mainapp.urls', namespace='products_urls')),
    path('history/', history, name='history_url'),
    path('showroom/', showroom, name='showroom_url'),
    path('contacts/', contacts, name='contacts_url'),
    path('basket/', include('basketapp.urls', namespace='basket_urls')),
    path('admin_custom/', include('adminapp.urls', namespace='admin_custom_urls')),
    path('social/', include('social_django.urls', namespace='social')),
    path('order/', include('ordersapp.urls', namespace='order_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
