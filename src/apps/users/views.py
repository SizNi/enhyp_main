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
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.info(
                    request, _("Пользователь успешно зарегистрирован и залогинен")
                )
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
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            messages.info(request, _("Профиль изменен"))
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("home")
        else:
            context["update_form"] = form
            context["pk"] = user_id
            return render(request, "users/update.html", context)
