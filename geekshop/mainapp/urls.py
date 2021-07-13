from django.urls import path
from .views import category, products, product_page


urlpatterns = [
    path('', products, name='products'),
    path('category/<int:pk>/', category, name='category'),
    path('product/<int:pk>/', product_page, name='product_page'),
]
