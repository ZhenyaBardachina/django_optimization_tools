from django.contrib.auth import get_user_model
from django.db import models
from mainapp.models import Product

# Create your models here.


class Basket(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('количество', default=0)
    add_datatime = models.DateTimeField('время', auto_now_add=True)
    upd_datatime = models.DateTimeField('время', auto_now=True)


    @property
    def product_cost(self):
        return self.product.price * self.quantity




