import secrets

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from config import settings
from users.forms import RegisterForm
from users.models import User


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}'
        send_mail(
            'Регистрация Skystore',
            f'Для подтверждения регистрации перейдите по ссылке {url}',
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class GeneratePasswordView(PasswordResetView):
    model = User
    form_class = PasswordResetForm
    template_name = 'users/generate.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.object = form.save()
        password = self.object.make_random_password(12)
        self.object.set_password(password)
        self.object.save()
        send_mail(
                    'Смена пароля Skystore',
                    f'Ваш новый пароль: {self.object.password}',
                    settings.EMAIL_HOST_USER,
                    [self.object.email]
                        )

        return super().form_valid(form)
