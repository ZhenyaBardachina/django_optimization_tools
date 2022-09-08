from django.shortcuts import render
from basketapp.models import Basket


def main(request):
    basket = ''
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    context = {
        'page_title': 'главная',
    }
    return render(request, 'index.html', context)


def contact(request):
    locations = [
        {'city': 'Екатеринбург',
         'phone': '+7-777-777-7777',
         'email': 'ekb-info@geekshop.ru',
         'address': 'В пределах ЕКАД'
         },
        {'city': 'Москва',
         'phone': '+7-888-888-8888',
         'email': 'msk-info@geekshop.ru',
         'address': 'В пределах МКАД'
         },
        {'city': 'Санкт-Петербург',
         'phone': '+7-999-999-9999',
         'email': 'spb-info@geekshop.ru',
         'address': 'В пределах КАД'
         },
    ]
    context = {
        'page_title': 'контакты',
        'locations': locations,
    }
    return render(request, 'contact.html', context)
