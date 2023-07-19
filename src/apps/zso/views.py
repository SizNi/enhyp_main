from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.zso.forms import ZsoFirstCreateForm
from django.http import HttpResponse
from apps.zso.models import Zso
import json


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
            zso_id = zso.id
            return redirect("zso_create_second", pk=zso_id)
        else:
            context["create_form"] = form
            return render(request, "zso/create.html", context)


@method_decorator(login_required, name="dispatch")
class ZsoSecondCreateView(UpdateView):
    def get(self, request, *args, **kwargs):
        zso_id = kwargs.get("pk")
        zso = Zso.objects.get(id=zso_id)
        well_numbers = zso.well_numbers
        context = {"well_numbers": range(1, well_numbers + 1)}
        return render(request, "zso/create_second.html", context)

    def post(self, request, *args, **kwargs):
        form = dict(request.POST)
        zso_id = kwargs.get("pk")
        zso = Zso.objects.get(id=zso_id)
        debit_list = []
        for i in range(1, len(form) + 1):
            field_name = f"debits_{i}"
            debits_value = form.get(field_name)
            if debits_value:
                debit_list.append(float(debits_value[0]))
        # сериализация для записи в бд test = json.loads(debit_json)
        debit_json = json.dumps(debit_list)
        zso.debits = debit_json
        zso.save()
        # тут будет модуль расчета
        return redirect("home")
