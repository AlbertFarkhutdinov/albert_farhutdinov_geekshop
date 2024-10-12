"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from shop.main_app.views import contacts, history, showroom
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('history/', history, name='history_url'),
    path('showroom/', showroom, name='showroom_url'),
    path('contacts/', contacts, name='contacts_url'),
    path(
        '',
        include(arg='main_app.urls', namespace='main_urls'),
    ),
    path(
        'auth/',
        include(arg='auth_app.urls', namespace='auth_urls'),
    ),
    path(
        'products/',
        include(arg='main_app.urls', namespace='products_urls'),
    ),
    path(
        'basket/',
        include(arg='basket_app.urls', namespace='basket_urls'),
    ),
    path(
        'admin_custom/',
        include(arg='admin_app.urls', namespace='admin_custom_urls'),
    ),
    path(
        'social/',
        include(arg='social_django.urls', namespace='social'),
    ),
    path(
        'order/',
        include(arg='orders_app.urls', namespace='order_urls'),
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
