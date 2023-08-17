from django.views.generic import ListView, TemplateView, DeleteView
from .models import WellSection
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from well_section_counter.handler import handler_front
from well_section_counter.main_counter import main
from apps.well_section.models import WellSection
from django.contrib import messages
from django.urls import reverse_lazy


@method_decorator(login_required, name="dispatch")
class WellSectionListView(ListView):
    model = WellSection
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        user_well_sections = request.user.well_section.all()
        return render(
            request,
            template_name="well_section/list.html",
            context={"well_sections": user_well_sections, "title": "Well sections"},
        )


# переписать
@method_decorator([csrf_exempt, login_required], name="dispatch")
class WellSectionCreateView(TemplateView):
    template_name = "well_section/create_form.html"

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
        zso_id = obj.id
        return JsonResponse({"url": f"/well_section/{zso_id}"})


@method_decorator(login_required, name="dispatch")
class WellSectionResultView(TemplateView):
    template_name = "well_section/result.html"

    def get(self, request, *args, **kwargs):
        context = {}
        ws_id = kwargs.get("pk")
        ws = WellSection.objects.get(id=ws_id)
        context["project_name"] = json.loads(ws.name)
        ws_data = {
            "layers": json.loads(ws.layers),
            "well_data": json.loads(ws.well_data),
        }
        image = main(ws_data)
        context["image"] = image
        messages.success(self.request, "Разрез скважины успешно построен")
        return render(request, "well_section/result.html", context)


@method_decorator(login_required, name="dispatch")
class WellSectionDeleteView(DeleteView):
    model = WellSection
    template_name = "well_section/delete.html"
    success_url = reverse_lazy("well_section_list")
