from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib import auth
from shop.auth_app.forms import ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from .models import ShopUser
from shop.main_app.common_context import page_name
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
# from django.urls import reverse_lazy
# from django.views.generic.edit import UpdateView


def register(request):
    register_form = ShopUserRegisterForm()
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(data=request.POST, files=request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                print('Сообщение подтверждения регистрации отправлено')
                return HttpResponseRedirect(reverse('auth_urls:login'))
            else:
                print('Ошибка отправки сообщения подтверждения регистрации')
                return HttpResponseRedirect(reverse('auth_urls:login'))
    context = {
        'title': 'Регистрация',
        'register_form': register_form,
        'submit_label': 'Зарегистрироваться'
    }
    return render(request, 'auth_app/register.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            if request.POST.get('next'):
                return HttpResponseRedirect(request.POST.get('next'))
            else:
                return HttpResponseRedirect(reverse('main_urls:featured'))

    get_next = request.GET.get('next')
    context = {
        'title': 'Вход',
        'next': get_next
    }
    return render(request, 'auth_app/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main_urls:featured'))


@login_required
@transaction.atomic
def edit(request, pk):
    get_user = get_object_or_404(ShopUser, pk=pk)
    edit_form = ShopUserEditForm(instance=get_user)
    profile_form = ShopUserProfileEditForm(instance=get_user.shopuserprofile)
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=get_user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=get_user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth_urls:edit', kwargs={'pk': pk}))
    context = {
        'edit_form': edit_form,
        'profile_form': profile_form,
        'submit_label': 'Применить',
    }
    page_name(context, 'Edit profile')
    return render(request, 'auth_app/edit.html', context)


def send_verify_mail(user):
    verify_link = reverse('auth_urls:verify', args=[user.email, user.activation_key])
    title = f'Подтверждение учетной записи {user.username}'
    message = (f'Для подтверждения учетной записи {user.username} на портале ' +
               f'{settings.DOMAIN_NAME} перейдите по ссылке:\n' +
               f'{settings.DOMAIN_NAME}{verify_link}')
    return send_mail(
        title,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'auth_app/verification.html')
        else:
            print(f'Error activation user: {user}')
            return render(request, 'auth_app/verification.html')
    except Exception as e:
        print(f'Error activation user: {e.args}')
        return HttpResponseRedirect(reverse('main_urls:featured'))


# class EditView(UpdateView):
#     model = ShopUser
#     template_name = 'auth_app/edit.html'
#     fields = ('username', 'email', 'first_name', 'last_name', 'avatar', 'password', 'age')
#     success_url = reverse_lazy('main_urls:featured')
#
#     def get_context_data(self, **kwargs):
#         # user = super(EditView, self).get_form_kwargs()['instance']
#         context = super(EditView, self).get_context_data(**kwargs)
#         page_name(context, 'Edit profile')
#         context['submit_label'] = 'Применить'
#         # context['common_context'] = common_context(user)
#         return context
