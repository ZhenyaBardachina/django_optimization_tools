import random

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page, never_cache

from mainapp.models import Product, ProductCategory


def get_products():
    if settings.LOW_CACHE:
        key = 'all_products'
        products = cache.get(key)
        if products is None:
            products = Product.get_items()
            cache.set(key, products)
        return products
    return Product.get_items()


def get_products_by_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}_products'
        products = cache.get(key)
        if products is None:
            products = Product.get_items().filter(category_id=pk)
            cache.set(key, products)
        return products
    return Product.get_items().filter(category_id=pk)


# return some random product and render
def get_hot_product():
    product_ids = get_products().values_list('id', flat=True)
    random_id = random.choice(product_ids)
    return Product.objects.get(pk=random_id)
    # return random.choice(Product.objects.all())


def same_product(hot_product):
    return Product.get_items().filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]


# @never_cache
# @cache_page(3600)
def products(request):
    hot_product = get_hot_product()
    context = {
        'page_title': 'каталог',
        'hot_product': hot_product,
        'same_product': same_product(hot_product),
    }
    return render(request, 'products.html', context)


def category(request, pk=None):
    page_num = request.GET.get('page', 1)
    if pk == 0:
        category = {'pk': 0, 'name': 'все', }
        products = get_products()
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = get_products_by_category(pk)

    product_paginator = Paginator(products, 3)
    try:
        products = product_paginator.page(page_num)
    except PageNotAnInteger:
        products = product_paginator.page(1)
    except EmptyPage:
        products = product_paginator.page(product_paginator.num_pages)

    context = {
        'page_title': 'товары категории',
        'category': category,
        'products': products,
    }

    return render(request, 'category_products.html', context)


def product_page(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'page_title': 'страница продукта',
        'product': product,
    }
    return render(request, 'product_page.html', context)


def get_product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.filter(pk=pk).first()
        return JsonResponse(
            {'price': product and product.price or 0}
        )


