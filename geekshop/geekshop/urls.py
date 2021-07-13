from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from mainapp import urls
from . import settings
from .views import main, contact

app_name = 'geekshop'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', main, name='index'),
    path('contact/', contact, name='contact'),
    path('products/', include('mainapp.urls')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('orders/', include('ordersapp.urls', namespace='orders')),
    path('', include('social_django.urls', namespace='social')),
    path('my/admin/', include('adminapp.urls', namespace='my_admin')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)