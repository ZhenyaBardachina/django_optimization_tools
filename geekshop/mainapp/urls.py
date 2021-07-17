from django.urls import path
from .views import category, products, product_page
urlpatterns = [
    path('', products, name='products'),
    path('category/<pk>/', category, name='category'),
    path('product/<pk>/', product_page, name='product_page'),
]
