from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from apps.users.models import CustomUser
from apps.users.forms import (
    LoginUserForm,
    CreateUserForm,
    UpdateUserForm,
    RecoveryUserForm,
    SecondRecoveryUserForm,
)
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .confirmation import mail_confirmation, user_recovery
from django.utils import timezone
from datetime import timedelta


def index(request):
    return HttpResponse("users")


class LoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        form = LoginUserForm()
        next_url = request.GET.get("next", "/")
        context["next"] = next_url
        context["login_form"] = form
        return render(request, "users/login.html", context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = LoginUserForm(request.POST)
        next_url = request.POST.get("next", "/")

        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.info(request, _("Вы залогинены"))
                return redirect(next_url)
        messages.error(
            request,
            _(
                "Пожалуйста, введите правильные имя пользователя и пароль."
                "Оба поля могут быть чувствительны к регистру."
            ),
        )
        context["login_form"] = form
        context["next"] = next_url
        return render(request, "users/login.html", context)


class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        messages.info(request, _("Вы разлогинены"))
        logout(request)
        return redirect("home")


class CreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {}
        form = CreateUserForm()
        context["registration_form"] = form
        return render(request, "users/create.html", context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(
                    request,
                    _(
                        "Пользователь успешно зарегистрирован и залогинен. Подтвердите вашу почту"
                    ),
                )
                try:
                    # функция отправки почты для верифицкации
                    mail_confirmation(user)
                except Exception as e:
                    messages.error(
                        request,
                        _(
                            "Произошла ошибка при отправке письма с подтверждением. Пожалуйста, свяжитесь с администратором."
                        ),
                    )
                    print(f"Ошибка отправки почты: {e}")
                return redirect("home")
        else:
            context["registration_form"] = form
            return render(request, "users/create.html", context)


@method_decorator(login_required, name="dispatch")
class UserUpdateView(UpdateView):
    def get(self, request, *args, **kwargs):
        current_user = request.user
        user_id = kwargs.get("pk")
        context = {}
        if current_user.id == user_id:
            user = CustomUser.objects.get(id=user_id)
            form = UpdateUserForm(instance=user)
            context["update_form"] = form
            context["pk"] = user_id
            return render(request, "users/update.html", context)
        else:
            messages.error(
                request, _("У вас нет прав для изменения другого пользователя.")
            )
            return redirect("home")

    def post(self, request, *args, **kwargs):
        context = {}
        user_id = kwargs.get("pk")
        user = CustomUser.objects.get(id=user_id)
        user_email = user.email
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            new_email = form.cleaned_data.get("email")
            username = form.cleaned_data.get("username")

            # если поменялся пароль
            if form.cleaned_data.get("password1"):
                password = form.cleaned_data.get("password1")
                user.set_password(password)
            else:
                password = user.password
            user = authenticate(username=username, password=password)
            user = CustomUser.objects.get(id=user_id)
            form.save()

            # если поменялся емейл
            if new_email != user_email:
                user.email = new_email
                user.save()
                login(request, user)
                try:
                    # функция отправки почты для верифицкации
                    mail_confirmation(user)
                    messages.info(
                        request,
                        _("Информация обновлена. Подтвердите вашу почту"),
                    )
                except Exception as e:
                    messages.error(
                        request,
                        _(
                            "Произошла ошибка при отправке письма с подтверждением. Пожалуйста, свяжитесь с администратором."
                        ),
                    )
                    print(f"Ошибка отправки почты: {e}")
                return redirect("home")
            else:
                messages.info(request, _("Профиль изменен"))
                return redirect("home")
        if user:
            login(request, user)
            return redirect("home")
        else:
            context["update_form"] = form
            context["pk"] = user_id
            return render(request, "users/update.html", context)


@method_decorator(login_required, name="dispatch")
class UserVerificationView(TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        # проверка, что пользователь авторизован
        if user is not None:
            verification_code = kwargs.get("verification_code")
            user_verification_code = user.confirmation_code
            expiration_time = user.confirmation_code_dt + timedelta(days=7)
            current_time = timezone.now()
            context = {}
            # устанавливаем срок действия ссылки
            if current_time > expiration_time:
                messages.error(
                    request,
                    _(
                        "Истек срок действия ссылки. Запросите новую в своем профиле"
                    ),  # новую надо реализовать
                )
                return redirect("user_update")
            # сраниваем коды верификации
            if (
                verification_code == user_verification_code
                and len(verification_code) != 0
            ):
                user.confirmed = True
                user.confirmation_code = ""
                user.save()
                context["email"] = user.email
                context["name"] = user.username
                messages.success(request, _("Почта подтверждена!"))
                return render(request, "users/mail_verification.html", context)
            else:
                messages.error(
                    request, _("Верификация не удалась, обратитесь к администратору")
                )
                return redirect("home")
        else:
            messages.error(request, _("Сначала залогиньтесь"))
            return redirect("user_login")


@method_decorator(login_required, name="dispatch")
class UserEmailConfirmationView(TemplateView):
    def get(self, request, *args, **kwargs):
        current_user = request.user
        user_id = kwargs.get("pk")
        context = {}
        if current_user.id == user_id:
            user = CustomUser.objects.get(id=user_id)
            context["name"] = user.username
            context["email"] = user.email
            try:
                # функция отправки почты для верифицкации
                mail_confirmation(user)
                messages.info(
                    request,
                    _("Письмо с подтверждением отправлено на почту"),
                )
            except Exception as e:
                messages.error(
                    request,
                    _(
                        "Произошла ошибка при отправке письма с подтверждением. Пожалуйста, свяжитесь с администратором."
                    ),
                )
                print(f"Ошибка отправки почты: {e}")
            return render(request, "users/send_email_confirmation.html", context)
        else:
            messages.error(
                request, _("У вас нет прав для изменения другого пользователя.")
            )
            return redirect("home")


class UserRecoveryView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        form = RecoveryUserForm()
        context["recovery_form"] = form
        return render(request, "users/recovery.html", context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = RecoveryUserForm(request.POST)
        context["recovery_form"] = form
        if form.is_valid():
            email = form.cleaned_data.get("email")
            try:
                user = CustomUser.objects.get(email=email)
                if user.confirmed == True:
                    # тут отправка емейла для восстановления
                    try:
                        user_recovery(user)
                        messages.info(
                            request,
                            _("Ссылка для восстановления отправлена вам на почту"),
                        )
                        return redirect("home")
                    except:
                        messages.error(
                            request,
                            _("Что-то пошло не так, свяжитесь с администрацией"),
                        )
                        return redirect("home")
                else:
                    messages.error(
                        request,
                        _("Почта не была подтверждена, свяжитесь с администрацией"),
                    )
                    return render(request, "users/recovery.html", context)
            except:
                messages.error(
                    request,
                    _("Почта не найдена"),
                )
                return render(request, "users/recovery.html", context)


# ввод нового пароля по ссылке восстановления
class UserRecoverySecondView(UpdateView):
    def get(self, request, *args, **kwargs):
        context = {}
        form = SecondRecoveryUserForm()
        context["recovery_form"] = form
        return render(request, "users/recovery_second.html", context)

    def post(self, request, *args, **kwargs):
        form = SecondRecoveryUserForm(request.POST)
        conf_code = kwargs.get("recovery_code")
        if form.is_valid():
            user = CustomUser.objects.get(confirmation_code=conf_code)
            # если почта была подтверждена - разрешаем сюда пойти
            if user.confirmed == True:
                password = form.cleaned_data.get("password")
                user.set_password(password)
                user.save()
                username = user.username
                user.conf_code = None
                user = authenticate(username=username, password=password)
                # если юзер существует
                if user is not None:
                    login(request, user)
                else:
                    messages.error(
                        request,
                        _("Что-то пошло не так, свяжитесь с администрацией"),
                    )
                    return redirect("home")
                messages.info(
                    request,
                    _("Пароль изменен, вход произведен"),
                )
                return redirect("home")
            else:
                messages.error(
                    request,
                    _("Ссылка недействительна"),
                )
                return redirect("home")
