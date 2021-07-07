from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from ordersapp.forms import OrderForm, OrderItemForm
from ordersapp.models import Order, OrderItem


# def index(request):
#     return render(request, 'ordersapp/index.html')


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return self.request.user.orders.all()


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem,
                                             form=OrderItemForm, extra=2)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, self.request.FILES)
        else:
            context['form'].initial['user'] = self.request.user
            basket_items = self.request.user.basket.all()
            if basket_items.exists():
                OrderFormSet = inlineformset_factory(
                    Order, OrderItem, form=OrderItemForm, extra=basket_items.count() + 1
                )
                formset = OrderFormSet()
                for form, basket_item in zip(formset.forms, basket_items):
                    form.initial['product'] = basket_item.product
                    form.initial['quantity'] = basket_item.quantity
            else:
                formset = OrderFormSet()

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            order = super().form_valid(form)
            if orderitems.is_valid():
                orderitems.instance = self.object  # one to many
                orderitems.save()
                self.request.user.basket.all().delete()

        # удаляем пустой заказ
        if self.object.total_cost() == 0:
            self.object.delete()

        return order


class OrderUpdate(UpdateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=3)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            order = super().form_valid(form)
            if orderitems.is_valid():
                orderitems.save()

        # удаляем пустой заказ
        if self.object.total_cost() == 0:
            self.object.delete()

        return order


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:delete')


class OrderRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        context['title'] = 'заказ/просмотр'
        return context


def forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('orders:index'))


