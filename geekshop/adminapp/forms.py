from django.contrib.auth import get_user_model
from django.forms import ModelForm, HiddenInput

from authapp.forms import ShopUserEditForm
from mainapp.models import ProductCategory, Product


class AdminShopUserUpdateForm(ShopUserEditForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'password', 'email', 'age', 'avatar', 'is_staff',
                  'is_superuser', 'is_active')

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     for field_name, field in self.fields.items():
        #         field.widget.attrs['class'] = 'form-control'
        #         field.help_text = ''
        #         if field_name.startswith('is_'):
        #             field.widget.attrs['class'] = CheckboxSelectMultiple()


class ProductCategoryCreateForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductUpdateForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'category':
                field.widget = HiddenInput()
