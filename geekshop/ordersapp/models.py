from django.contrib.auth import get_user_model
from django.db import models
from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(verbose_name='статус',
                              max_length=3,
                              choices=STATUS_CHOICES,
                              default=FORMING)
    is_active = models.BooleanField(verbose_name='активен', default=True)

    @property
    def is_forming(self):
        return self.status == self.FORMING

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    @property
    def total_quantity(self):
        return sum(map(lambda x: x.quantity, self.items.all()))

    @property
    def total_cost(self):
        return sum(map(lambda x: x.product_cost, self.items.all()))

    # переопределяем метод, удаляющий объект
    def delete(self, using=None, keep_parent=False):
        # for item in self.orderitems.select_related():
        #     item.product.quantity += item.quantity
        #     item.product.save()
        for item in self.items.all():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='items')
    product = models.ForeignKey(Product,
                                verbose_name='продукт',
                                on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name='количество',
                                           default=0)

    @property
    def product_cost(self):
        return self.product.price * self.quantity
