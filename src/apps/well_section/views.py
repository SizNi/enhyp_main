# views.py
from django.views.generic import ListView, TemplateView, CreateView
from .models import WellSection
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import FileResponse, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from well_section_counter.handler import handler_front


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
        # это в следующий вью
        image = handler_front(data_json)
        return JsonResponse({"url": "/"})

# дописать
@method_decorator(login_required, name="dispatch")
class WellSectionCreatedView(TemplateView):
    template_name = "well_section/create_form.html"

    def post(self, request, *args, **kwargs):
        data_json = json.loads(request.body)
        image = handler_front(data_json)
        print(data_json)
        print(type(data_json))
        return JsonResponse({"url": "/"})
