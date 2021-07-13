from django import template
from django.conf import settings

register = template.Library()


def media_folder_products(string):
    '''
    Добавит автоматический относительный url-путь к media
    /media/products_img/default.jpg -> products_img/default.jpg
    '''
    if not string:
        string = 'products_img/default.jpg'

    return f'{settings.MEDIA_URL}{string}'


@register.filter(name='media_folder_users')
def media_folder_users(string):
    '''
    Добавит автоматический относительный url-путь к media
    /media/avatars/default.jpg -> avatars/default.jpg
    '''
    if not string:
        string = 'user_avatars/_user.png'

    return f'{settings.MEDIA_URL}{string}'


register.filter('media_folder_products', media_folder_products)
