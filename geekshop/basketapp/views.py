from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from basketapp.models import Basket


from geekshop.settings import LOGIN_URL


@login_required
def index(request):
    basket = request.user.basket.all()
    context = {
        'page_title': 'корзина',
        'basket': basket,
    }
    return render(request, 'basketapp/index.html', context)


@login_required
def add(request, product_pk):
    if LOGIN_URL in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(
            reverse('product_page',
                    kwargs={'pk': product_pk}))

    basket_item, _ = Basket.objects.get_or_create(
        user=request.user,
        product_id=product_pk,
    )
    basket_item.quantity += 1
    basket_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, basket_item_pk):
    item = get_object_or_404(Basket, pk=basket_item_pk)
    item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update(request, basket_item_pk, quantity):
    if request.is_ajax():
        item = Basket.objects.filter(pk=basket_item_pk).first()
        if not item:
            return JsonResponse({'status': False})
        if quantity == 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()
        basket_summary_html = render_to_string('basketapp/includes/basket_summary.html', request=request)
        return JsonResponse({'status': True,
                             'basket_summary': basket_summary_html,
                             'quantity': quantity})
