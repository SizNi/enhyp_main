from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
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
        # получение данных
        form = request.POST
        zso_id = kwargs.get("pk")
        zso = Zso.objects.get(id=zso_id)
        debit_value = form.getlist("debits")
        x_value = form.getlist("x")
        y_value = form.getlist("y")
        # валидация и преобразование для записи в бд
        if (
            "" not in debit_value
            and "" not in x_value
            and "" not in y_value
            and len(y_value) != 0
        ):
            for elem in debit_value:
                elem = elem.replace(",", ".")
            debit_value = list(map(float, debit_value))
            debit_json = json.dumps(debit_value)
            for elem in x_value:
                elem = elem.replace(",", ".")
            x_value = list(map(int, x_value))
            x_json = json.dumps(x_value)
            for elem in y_value:
                elem = elem.replace(",", ".")
            y_value = list(map(int, y_value))
            y_json = json.dumps(y_value)
        else:
            well_numbers = zso.well_numbers
            context = {"well_numbers": range(1, well_numbers + 1)}
            messages.error(request, _("Некорректные данные: поля не заполнены"))
            return render(request, "zso/create_second.html", context)
        # сериализация для записи в бд и сохранение формы
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
