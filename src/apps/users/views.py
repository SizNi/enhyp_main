from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import TemplateView
from django.http import HttpResponse
from apps.users.forms import LoginUserForm
from django.utils.translation import gettext_lazy as _

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
                return redirect('users_home')
        messages.error(request, _(
            'Пожалуйста, введите правильные имя пользователя и пароль.'
            'Оба поля могут быть чувствительны к регистру.')
        )
        context['login_form'] = form
        return render(request, 'users/login.html', context)