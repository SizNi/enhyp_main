from django.views.generic import ListView, TemplateView, DeleteView, UpdateView, View
from .models import WellSection
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from well_section_counter.handler import handler_front
from well_section_counter.main_counter import main
from apps.well_section.models import WellSection
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page


@method_decorator(login_required, name="dispatch")
class WellSectionListView(ListView):
    model = WellSection
    paginate_by = 10
    template_name = ("well_section/list.html",)

    def get(self, request, *args, **kwargs):
        user_well_sections = request.user.well_section.all()
        well_sections = [
            {
                "name": section.get_deserialized_name(),
                "created_at": section.created_at,
                "id": section.id,
            }
            for section in user_well_sections
        ]
        return render(
            request,
            template_name=self.template_name,
            context={"well_sections": well_sections, "title": "Well sections"},
        )


# добавить на фронте обработчик ссылки
@method_decorator([csrf_exempt, login_required], name="dispatch")
class WellSectionCreateView(TemplateView):
    template_name = "well_section/form.html"

    def post(self, request, *args, **kwargs):
        # это в бд
        data_json = json.loads(request.body)
        work_data = handler_front(data_json)
        obj = WellSection()
        obj.user = request.user
        obj.name = json.dumps(work_data["project_name"])
        obj.layers = json.dumps(work_data["layers"])
        obj.well_data = json.dumps(work_data["well_data"])
        obj.save()
        obj_id = obj.id
        url = reverse_lazy("well_section_result", args=[obj_id])
        return JsonResponse({"url": url, "status": 200})


@method_decorator(cache_page(900), name="dispatch")
@method_decorator(login_required, name="dispatch")
class WellSectionResultView(TemplateView):
    template_name = "well_section/result.html"

    def get(self, request, *args, **kwargs):
        ws_id = kwargs.get("pk")
        ws = WellSection.objects.get(id=ws_id)
        context = {"project_name": json.loads(ws.name)}
        ws_data = {
            "layers": json.loads(ws.layers),
            "well_data": json.loads(ws.well_data),
        }
        print(ws_data)
        context = {"image": main(ws_data)}
        messages.success(self.request, "Разрез скважины успешно построен")
        return render(request, "well_section/result.html", context)


@method_decorator(login_required, name="dispatch")
class WellSectionDeleteView(DeleteView):
    model = WellSection
    template_name = "well_section/delete.html"
    success_url = reverse_lazy("well_section_list")


# доработать
@method_decorator([csrf_exempt, login_required], name="dispatch")
class WellSectionUpdateView(TemplateView):
    model = WellSection
    template_name = "well_section/update.html"  # Укажите ваш шаблон
    success_url = "/success/"  # Укажите URL для редиректа после успешного обновления

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Получение данных из запроса
        data_json = json.loads(request.body)
        work_data = handler_front(data_json)

        # Обновление данных объекта
        self.object.name = json.dumps(work_data["project_name"])
        self.object.layers = json.dumps(work_data["layers"])
        self.object.well_data = json.dumps(work_data["well_data"])
        self.object.save()

        # Формирование URL для редиректа
        url = reverse_lazy("well_section_result", args=[self.object.id])

        return JsonResponse({"url": url, "status": 200})
