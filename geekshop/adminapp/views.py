from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView

from adminapp.forms import AdminShopUserUpdateForm, ProductCategoryCreateForm, ProductUpdateForm
from mainapp.models import ProductCategory, Product


class SuperUserOnlyMixin:
    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PageTitleMixin:
    page_title_key = 'page_title'
    page_title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.page_title_key] = self.page_title
        return context


@user_passes_test(lambda user: user.is_superuser)
def index(request):
    all_users = get_user_model().objects.all()
    context = {
        'page_title': 'админка/пользователи',
        'all_users': all_users,
    }
    return render(request, 'adminapp/index.html', context)


# @user_passes_test(lambda user: user.is_superuser)
# def user_update(request, user_pk):
#     user = get_object_or_404(get_user_model(), pk=user_pk)
#     if request.method == 'POST':
#         user_form = AdminShopUserUpdateForm(request.POST, request.FILES, instance=user)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('my_admin:index'))
#     else:
#         user_form = AdminShopUserUpdateForm(instance=user)
#
#     context = {
#         'page_title': 'админка/пользователи/редактирование',
#         'user_form': user_form,
#     }
#
#     return render(request, 'adminapp/shopuser_form.html', context)


class ShopUserAdminUpdate(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = get_user_model()
    form_class = AdminShopUserUpdateForm
    success_url = reverse_lazy('my_admin:index')
    pk_url_kwarg = 'user_pk'
    page_title = 'пользователи/редактирование'


@user_passes_test(lambda user: user.is_superuser)
def user_delete(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    if not user.is_active or request.method == 'POST':
        if user.is_active:
            user.is_active = False
            user.save()
        return HttpResponseRedirect(reverse('my_admin:index'))
    context = {
        'page_title': 'админка/пользователи/удаление',
        'user': user,
    }
    return render(request, 'adminapp/user_delete.html', context)


# @user_passes_test(lambda user: user.is_superuser)
# def categories(request):
#     context = {
#         'page_title': 'админка/категории',
#         'categories_list': ProductCategory.objects.all()
#     }
#     return render(request, 'adminapp/productcategory_list.html', context)


class ProductCategoryList(SuperUserOnlyMixin, PageTitleMixin, ListView):
    model = ProductCategory
    page_title = 'категории'


class ProductCategoryCreate(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = ProductCategory
    form_class = ProductCategoryCreateForm
    success_url = reverse_lazy('my_admin:categories')
    page_title = 'категории/создание'
    # fields = '__all__'
    # template_name = 'adminapp/productcategory_form.html'


class ProductCategoryUpdate(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = ProductCategory
    form_class = ProductCategoryCreateForm
    success_url = reverse_lazy('my_admin:categories')
    page_title = 'категории/редактирование'


class ProductCategoryDelete(SuperUserOnlyMixin, PageTitleMixin, DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('my_admin:categories')
    page_title = 'категории/удаление'


@user_passes_test(lambda user: user.is_superuser)
def category_products(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    object_list = category.product_set.all()
    context = {
        'page_title': f'категория {category.name}/продукты',
        'category': category,
        'object_list': object_list,
    }
    return render(request, 'mainapp/category_product_list.html', context)


@user_passes_test(lambda user: user.is_superuser)
def category_product_create(request, category_pk):
    category = get_object_or_404(ProductCategory, pk=category_pk)
    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('my_admin:category_products', kwargs={'pk': category.pk}))
    else:
        form = ProductUpdateForm(initial={'category': category, })

    context = {
        'page_title': 'продукты/создание',
        'form': form,
        'category': category
    }
    return render(request, 'mainapp/product_update.html', context)


@user_passes_test(lambda user: user.is_superuser)
def product_delete(request, pk):
    object = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        object.is_active = False
        object.save()
        return HttpResponseRedirect(reverse('my_admin:category_products', kwargs={'pk': object.category.pk}))

    context = {
        'page_title': 'продукты/удаление',
        'object': object,
    }
    return render(request, 'mainapp/product_delete.html', context)


class ProductDetail(SuperUserOnlyMixin, PageTitleMixin, DetailView):
    model = Product
    page_title = 'админка/продукты'
