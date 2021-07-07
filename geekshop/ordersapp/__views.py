from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, DetailView
from ordersapp.forms import OrderForm, OrderItemForm
from ordersapp.models import Order, OrderItem


def index(request):
    return render(request, 'ordersapp/index.html')


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return self.request.user.orders.all()


class OrderItemsCreate(CreateView):
   model = Order
   fields = []
   success_url = reverse_lazy('ordersapp:orders_list')

   def get_context_data(self, **kwargs):
       data = super(OrderItemsCreate, self).get_context_data(**kwargs)
       OrderFormSet = inlineformset_factory(Order, OrderItem, \
                                            form=OrderItemForm, extra=1)

       if self.request.POST:
           formset = OrderFormSet(self.request.POST)
       else:
           basket_items = Basket.get_items(self.request.user)
           if len(basket_items):
               OrderFormSet = inlineformset_factory(Order, OrderItem, \
                                  form=OrderItemForm, extra=len(basket_items))
               formset = OrderFormSet()
               for num, form in enumerate(formset.forms):
                   form.initial['product'] = basket_items[num].product
                   form.initial['quantity'] = basket_items[num].quantity
               basket_items.delete()
           else:
               formset = OrderFormSet()

       data['orderitems'] = formset
       return data

   def form_valid(self, form):
       context = self.get_context_data()
       orderitems = context['orderitems']

       with transaction.atomic():
           form.instance.user = self.request.user
           self.object = form.save()
           if orderitems.is_valid():
               orderitems.instance = self.object
               orderitems.save()

       # удаляем пустой заказ
       if self.object.total_cost() == 0:
           self.object.delete()

       return super(OrderItemsCreate, self).form_valid(form)