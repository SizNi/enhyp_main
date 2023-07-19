from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.zso.forms import ZsoFirstCreateForm, ZsoSecondCreateForm
from django.http import HttpResponse


def index(request):
    return HttpResponse("zso")


@method_decorator(login_required, name="dispatch")
class ZsoFirstCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {}
        form = ZsoFirstCreateForm()
        context["create_form"] = form
        return render(request, "zso/create.html", context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = ZsoFirstCreateForm(request.POST)
        if form.is_valid():
            zso = form.save(commit=False)
            zso.user = request.user
            zso.save()
            return redirect("zso_create_second")
        else:
            context["create_form"] = form
            return render(request, "zso/create.html", context)


@method_decorator(login_required, name="dispatch")
class ZsoSecondCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        zso_id = kwargs.get("pk")
        context = {}
        form = ZsoSecondCreateForm()
        context["create_form"] = form
        return render(request, "zso/create_second.html", context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = ZsoFirstCreateForm(request.POST)
        if form.is_valid():
            zso = form.save(commit=False)
            zso.user = request.user
            zso.save()
            return redirect("zso_create_second")
        else:
            context["create_form"] = form
            return render(request, "zso/create.html", context)
