from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import TemplateView, CreateView
from django.http import HttpResponse
from apps.users.forms import LoginUserForm, CreateUserForm
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

def index(request):
    return HttpResponse('users')


class LoginView(TemplateView):

    def get(self, request, *args, **kwargs):
        context = {}
        form = LoginUserForm()
        context['login_form'] = form
        return render(request, 'users/login.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = LoginUserForm(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                messages.info(request, _('Вы залогинены'))
                return redirect('home')
        messages.error(request, _(
            'Пожалуйста, введите правильные имя пользователя и пароль.'
            'Оба поля могут быть чувствительны к регистру.')
        )
        context['login_form'] = form
        return render(request, 'users/login.html', context)


class LogoutView(TemplateView):

    def get(self, request, *args, **kwargs):
        messages.info(request, _('Вы разлогинены'))
        logout(request)
        return redirect('home')


class CreateView(CreateView):

    def get(self, request, *args, **kwargs):
        context = {}
        form = CreateUserForm()
        context['registration_form'] = form
        return render(request, 'users/create.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.info(request, _('Пользователь успешно зарегистрирован и залогинен'))
                return redirect('users_home')
        else:
            context['registration_form'] = form
            return render(request, 'users/create.html', context)