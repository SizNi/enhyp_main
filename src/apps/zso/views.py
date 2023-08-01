from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.zso.forms import ZsoFirstCreateForm
from django.http import HttpResponse
from apps.zso.models import Zso
from apps.zso.call_counter import counter
import json
import base64


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
        x_list = []
        y_list = []
        # получение данных из формы (надо бы добавить туда проверок)
        for i in range(1, len(form) + 1):
            field_name = f"debits_{i}"
            debits_value = form.get(field_name)
            if debits_value:
                debit_list.append(float(debits_value[0]))
            field_name = f"x_{i}"
            x_value = form.get(field_name)
            if debits_value:
                x_list.append(int(x_value[0]))
            field_name = f"y_{i}"
            y_value = form.get(field_name)
            if debits_value:
                y_list.append(int(y_value[0]))
        # сериализация для записи в бд и сохранение формы
        debit_json = json.dumps(debit_list)
        x_json = json.dumps(x_list)
        y_json = json.dumps(y_list)
        zso.n_x_skv = x_json
        zso.n_y_skv = y_json
        zso.debits = debit_json
        zso.save()
        # получение результирующай картинки и датасета из обработчика
        image, main_dataset = counter(zso.id)
        # преобразование датасета (картинка преобразуется в обработчике)
        main_df_bytes = main_dataset.to_csv(index=False).encode("utf-8")
        main_df_base64 = base64.b64encode(main_df_bytes).decode("utf-8")
        # отправка на фронт
        if image is not False:
            image_data = base64.b64encode(image.getvalue()).decode("utf-8")
            context = {}
            context["image"] = image_data
            context["df"] = main_df_base64
            messages.info(request, _("Расчет завершен!"))
            return render(request, "zso/result.html", context)
        else:
            context = {}
            context["warning"] = "Что-то пошло не так"
            return render(request, "zso/mistake.html", context)
