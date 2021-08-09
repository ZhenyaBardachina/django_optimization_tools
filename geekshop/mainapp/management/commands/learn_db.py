from django.db.models import Q
from mainapp.models import Product
from django.core.management import BaseCommand


# def sample_1():
#     cat_1 = Q(category__name= 'дом')
#     cat_2 = Q(category__name= 'модерн')
#     product_list = Product.objects.filter(cat_1 | cat_2)
#
#     print(product_list)

class Command(BaseCommand):

    def handle(self, *args, **options):
        from datetime import timedelta
        from django.db.models import F, When, Case, DecimalField, IntegerField
        from ordersapp.models import OrderItem


        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_EXPIRED = 3

        action_1__time_delta = timedelta(hours=12)
        action_2__time_delta = timedelta(hours=24)

        action_1_discount = 0.3
        action_2_discount = 0.15
        action_expired_discount = 0.05

        action_1__condition = Q(order__updated__lte=F('order__created') + action_1__time_delta)
        action_2__condition = Q(order__updated__gt=F('order__created') + action_1__time_delta) & \
                              Q(order__updated__lte=F('order__created') + action_2__time_delta)
        action_expired__condition = Q(order__updated__gt=F('order__created') + action_2__time_delta)

        action_1__order = When(action_1__condition, then=ACTION_1)
        action_2__order = When(action_2__condition, then=ACTION_2)
        action_expired__order = When(action_expired__condition, then=ACTION_EXPIRED)

        action_1__price = When(action_1__condition,
                               then=F('product__price') * F('quantity') * action_1_discount)

        action_2__price = When(action_2__condition,
                               then=F('product__price') * F('quantity') * -action_2_discount)

        action_expired__price = When(action_expired__condition,
                                     then=F('product__price') * F('quantity') * action_expired_discount)

        best_orderitems = OrderItem.objects.annotate(
            action_order=Case(
                action_1__order,
                action_2__order,
                action_expired__order,
                output_field=IntegerField(),
            )).annotate(
            discount=Case(
                action_1__price,
                action_2__price,
                action_expired__price,
                output_field=DecimalField(),
            )).order_by('action_order', 'discount').select_related('order', 'product')

        for orderitem in best_orderitems:
            print(f'{orderitem.action_order:2}: заказ №{orderitem.pk:3}:\
                       {orderitem.product.name:15}: скидка\
                       {abs(orderitem.discount):6.2f} руб. | \
                       {orderitem.order.updated - orderitem.order.created}')


# if __name__ == '__main__':
#     sample()
