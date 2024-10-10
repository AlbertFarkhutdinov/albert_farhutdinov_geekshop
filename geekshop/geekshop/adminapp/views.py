from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.views.generic.list import ListView
from mainapp.models import Product, ProductCategory
from authapp.models import ShopUser
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection
from adminapp.forms import ProductCategoryEditForm
from django.db.models import F


@user_passes_test(lambda u: u.is_superuser)
def main_admin_page(request):
    context = {
        'title': 'Администрирование сайта'
    }
    return render(request, 'adminapp/index.html', context)


class IsSuperUserView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class ProductListView(IsSuperUserView, ListView):
    model = Product
    template_name = 'adminapp/products.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        context['title'] = 'Список продуктов'
        context['product_categories'] = ProductCategory.objects.all()
        return context

    def get_queryset(self):
        queryset = Product.objects.all()
        category_pk = self.kwargs.get('category_pk')
        if category_pk:
            queryset = queryset.filter(category=category_pk)
        return queryset


class CategoryListView(IsSuperUserView, ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data()
        context['title'] = 'Категории продуктов'
        return context


class UserListView(IsSuperUserView, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data()
        context['title'] = 'Пользователи'
        return context


class ProductDetailView(IsSuperUserView, DetailView):
    model = Product
    template_name = 'adminapp/product.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        context['title'] = self.object.name
        return context


class ProductCreateView(IsSuperUserView, CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data()
        context['title'] = 'Создание нового продукта'
        context['button_label'] = 'Создать'
        return context

    def get_success_url(self):
        return reverse_lazy('admin_custom_urls:products')

    def form_valid(self, form):
        instance = form.save()
        print(instance.pk)
        return redirect(self.get_success_url() + str(instance.pk))


class CategoryCreateView(IsSuperUserView, CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_custom_urls:categories')

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data()
        context['title'] = 'Создание новой категории'
        context['button_label'] = 'Создать'
        return context


class UserCreateView(IsSuperUserView, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_custom_urls:users')

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data()
        context['title'] = 'Создание нового пользователя'
        context['button_label'] = 'Создать'
        return context


class ProductUpdateView(IsSuperUserView, UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data()
        context['title'] = 'Редактирование продукта'
        context['button_label'] = 'Применить'
        return context

    def get_success_url(self):
        return reverse_lazy('admin_custom_urls:product_read', kwargs={'pk': self.kwargs.get('pk')})


class CategoryUpdateView(IsSuperUserView, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    # fields = '__all__'
    success_url = reverse_lazy('admin_custom_urls:categories')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        context['button_label'] = 'Применить'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)
        return super().form_valid(form)


class UserUpdateView(IsSuperUserView, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_custom_urls:users')

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data()
        context['title'] = self.object.username
        context['button_label'] = 'Применить'
        return context


class ProductDeleteView(IsSuperUserView, DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    success_url = reverse_lazy('admin_custom_urls:products')

    def get_context_data(self, **kwargs):
        context = super(ProductDeleteView, self).get_context_data()
        context['title'] = 'Удаление продукта'
        context['cancel_page'] = 'admin_custom_urls:products'


class CategoryDeleteView(IsSuperUserView, DeleteView):
    model = ProductCategory
    template_name = 'adminapp/product_delete.html'
    success_url = reverse_lazy('admin_custom_urls:categories')

    def get_context_data(self, **kwargs):
        context = super(CategoryDeleteView, self).get_context_data()
        context['title'] = 'Удаление категории'
        context['cancel_page'] = 'admin_custom_urls:categories'


class UserDeleteView(IsSuperUserView, DeleteView):
    model = ShopUser
    template_name = 'adminapp/product_delete.html'
    success_url = reverse_lazy('admin_custom_urls:users')

    def get_context_data(self, **kwargs):
        context = super(UserDeleteView, self).get_context_data()
        context['title'] = 'Удаление пользователя'
        context['cancel_page'] = self.success_url


def db_profile_by_type(prefix, _type, queries):
    update_queries = list(filter(lambda x: _type in x['sql'], queries))
    # print(f'db_profile {_type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_product_category_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
    else:
        instance.product_set.update(is_active=False)
    db_profile_by_type(sender, 'UPDATE', connection.queries)
