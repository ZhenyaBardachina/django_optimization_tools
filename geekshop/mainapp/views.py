import random
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from mainapp.models import Product, ProductCategory


# return some random product and render
def get_hot_product():
    product_ids = Product.get_items().values_list('id', flat=True)
    random_id = random.choice(product_ids)
    return Product.objects.get(pk=random_id)
    # return random.choice(Product.objects.all())


def same_product(hot_product):
    return Product.get_items().filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]

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
        products = Product.get_items()
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = category.product_set.filter(is_active=True)
        # products = Product.objects.filter(category__pk=pk)

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


