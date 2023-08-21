from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from apps.users.models import CustomUser
from apps.users.forms import LoginUserForm, CreateUserForm, UpdateUserForm
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.conf import settings


def index(request):
    return HttpResponse("users")


class LoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        form = LoginUserForm()
        next_url = request.GET.get("next", "/")
        print(next_url)
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

                print(next_url)
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
            email = form.cleaned_data.get("email")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.info(
                    request, _("Пользователь успешно зарегистрирован и залогинен. Подтвердите вашу почту")
                )
                try:
                    mail_confirmation(username, email, 'reg')
                except Exception as e:
                    messages.error(request, _("Произошла ошибка при отправке письма с подтверждением. Пожалуйста, свяжитесь с администратором."))
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

    def post(self, request, *args, **kwargs): # изменение работает некорректно, нельзя оставить старое имя пользователя и при пустом поле пароля все сбивается
        context = {}
        user_id = kwargs.get("pk")
        user = CustomUser.objects.get(id=user_id)
        user_email = user.email
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            new_email = form.cleaned_data.get("email")
            username = form.cleaned_data.get("username")
            print(form.cleaned_data.get("password1"))
            if form.cleaned_data.get("password1"):
                password = form.cleaned_data.get("password1")
                user.set_password(password)
                print('hoho')
            else:
                password = user.password
            user = authenticate(username=username, password=password)
            form.save()
            if new_email != user_email:
                try:
                    mail_confirmation(username, new_email, 'upd')
                    messages.info(request, _("Профиль изменен, письмо с подтверждением для нового почтового адреса отправлено"))
                except Exception as e:
                    messages.error(request, _("Произошла ошибка при отправке письма с подтверждением. Пожалуйста, свяжитесь с администратором."))
                    print(f"Ошибка отправки почты: {e}")
            else:
                messages.info(request, _("Профиль изменен"))
            if user:
                login(request, user)
                return redirect("home")
        else:
            context["update_form"] = form
            context["pk"] = user_id
            return render(request, "users/update.html", context)


def mail_confirmation(username, user_mail, status):
        message = f"""
            Добрый день, {username}, для подтверждения адреса перейдите по ссылке:<br>
            <a href="https://enhyp.ru/">ссылка</a>
            """
        send_mail(
            "Подтверждение почтового адреса",
            f"Добрый день, {username}, для подтверждения адреса перейдите по ссылке",
            settings.EMAIL_HOST_USER,
            [f"{user_mail}"],
            # ["q7j4lypoikqg@mail.ru"],
            fail_silently=False,
            html_message=message,
        )
