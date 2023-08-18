from django.views.generic import ListView, TemplateView, DeleteView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from well_section_counter.handler import handler_front
from well_section_counter.main_counter import main
from apps.well_passport.models import WellPassport
from django.contrib import messages
from django.urls import reverse_lazy


@method_decorator(login_required, name="dispatch")
class WellPassportListView(ListView):
    model = WellPassport
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        user_well_sections = request.user.well_passport.all()
        return render(
            request,
            template_name="well_section/list.html",
            context={"well_sections": user_well_sections, "title": "Well sections"},
        )
