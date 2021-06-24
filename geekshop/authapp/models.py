from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст')

    def basket_price(self):
        return sum(el.product_cost for el in self.basket.all())

    def basket_quantity(self):
        return sum(el.quantity for el in self.basket.all())

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def is_activation_key_expired(self):
        if now() < self.activation_key_created + timedelta(hours=48):
            return False
        return True
