from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import connection, models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from shop.admin_app.forms import ProductCategoryEditForm
from shop.auth_app.models import ShopUser
from shop.main_app.models import Product, ProductCategory

TITLE = 'title'
BUTTON_LABEL = 'button_label'
ALL_FIELDS = '__all__'
SUCCESS_URL = 'admin_custom_urls:categories'


@user_passes_test(lambda user: user.is_superuser)
def main_admin_page(request):
    context = {
        TITLE: 'Admin Page',
    }
    return render(request, 'admin_app/index.html', context)


class IsSuperUserView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class ProductListView(IsSuperUserView, ListView):
    model = Product
    template_name = 'admin_app/products.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context[TITLE] = 'Product List'
        context['product_categories'] = ProductCategory.categories.all()
        return context

    def get_queryset(self):
        queryset = Product.products.all()
        category_pk = self.kwargs.get('category_pk')
        if category_pk:
            return queryset.filter(category=category_pk)
        return queryset


class CategoryListView(IsSuperUserView, ListView):
    model = ProductCategory
    template_name = 'admin_app/categories.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context[TITLE] = 'Product Categories'
        return context


class UserListView(IsSuperUserView, ListView):
    model = ShopUser
    template_name = 'admin_app/users.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context[TITLE] = 'Users'
        return context


class ProductDetailView(IsSuperUserView, DetailView):
    model = Product
    template_name = 'admin_app/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = self.object.name
        return context


class ProductCreateView(IsSuperUserView, CreateView):
    model = Product
    template_name = 'admin_app/product_update.html'
    fields = ALL_FIELDS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = 'New Item Creating'
        context[BUTTON_LABEL] = 'Create'
        return context

    def get_success_url(self):
        return reverse_lazy('admin_custom_urls:products')

    def form_valid(self, form):
        instance = form.save()
        print(instance.pk)
        return redirect(self.get_success_url() + str(instance.pk))


class CategoryCreateView(IsSuperUserView, CreateView):
    model = ProductCategory
    template_name = 'admin_app/category_update.html'
    fields = ALL_FIELDS
    success_url = reverse_lazy(SUCCESS_URL)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = 'New Item Creating'
        context[BUTTON_LABEL] = 'Create'
        return context


class UserCreateView(IsSuperUserView, CreateView):
    model = ShopUser
    template_name = 'admin_app/user_update.html'
    fields = ALL_FIELDS
    success_url = reverse_lazy('admin_custom_urls:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = 'New Item Creating'
        context[BUTTON_LABEL] = 'Create'
        return context


class ProductUpdateView(IsSuperUserView, UpdateView):
    model = Product
    template_name = 'admin_app/product_update.html'
    fields = ALL_FIELDS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = 'Product Update'
        context[BUTTON_LABEL] = 'Apply'
        return context

    def get_success_url(self):
        return reverse_lazy(
            'admin_custom_urls:product_read',
            kwargs={'pk': self.kwargs.get('pk')},
        )


class CategoryUpdateView(IsSuperUserView, UpdateView):
    model = ProductCategory
    template_name = 'admin_app/category_update.html'
    # fields = ALL_FIELDS
    success_url = reverse_lazy(SUCCESS_URL)
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = self.object.name
        context[BUTTON_LABEL] = 'Apply'
        return context

    def form_valid(self, form):
        discount = form.cleaned_data.get('discount', 0)
        if discount:
            self.object.product_set.update(
                price=models.F('price') * (1 - discount / 100),
            )
            db_profile_by_type(
                prefix=self.__class__,
                _type='UPDATE',
                queries=connection.queries,
            )
        return super().form_valid(form)


class UserUpdateView(IsSuperUserView, UpdateView):
    model = ShopUser
    template_name = 'admin_app/user_update.html'
    fields = ALL_FIELDS
    success_url = reverse_lazy('admin_custom_urls:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = self.object.username
        context[BUTTON_LABEL] = 'Apply'
        return context


class ProductDeleteView(IsSuperUserView, DeleteView):
    model = Product
    template_name = 'admin_app/product_delete.html'
    success_url = reverse_lazy('admin_custom_urls:products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = 'Delete Product'
        context['cancel_page'] = 'admin_custom_urls:products'


class CategoryDeleteView(IsSuperUserView, DeleteView):
    model = ProductCategory
    template_name = 'admin_app/product_delete.html'
    success_url = reverse_lazy(SUCCESS_URL)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = 'Delete Category'
        context['cancel_page'] = SUCCESS_URL


class UserDeleteView(IsSuperUserView, DeleteView):
    model = ShopUser
    template_name = 'admin_app/product_delete.html'
    success_url = reverse_lazy('admin_custom_urls:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = 'Delete User'
        context['cancel_page'] = self.success_url


def db_profile_by_type(prefix, _type, queries):
    update_queries = list(filter(lambda query: _type in query['sql'], queries))
    # print(f'db_profile {_type} for {prefix}:')
    for query in update_queries:
        print(query['sql'])


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_product_category_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
    else:
        instance.product_set.update(is_active=False)
    db_profile_by_type(sender, 'UPDATE', connection.queries)
