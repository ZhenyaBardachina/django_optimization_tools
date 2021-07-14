from django import forms
from django.forms import HiddenInput

from mainapp.models import Product
from ordersapp.models import Order, OrderItem


class BaseOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'user':
                field.widget = HiddenInput()
            field.widget.attrs['class'] = 'form-control'


class OrderForm(BaseOrderForm):
    class Meta:
        model = Order
        fields = ('user',)


class OrderItemForm(BaseOrderForm):
    price = forms.FloatField(label='цена за 1 ед', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.get_items()

    # Не работает
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        product = self.cleaned_data.get('product')
        if quantity > product.quantity:
            raise forms.ValidationError("Недостаточно товара на складе!")
        return quantity


    class Meta:
        model = OrderItem
        fields = '__all__'
