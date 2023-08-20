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
from apps.organizations.models import Organization
from django.contrib import messages
from django.urls import reverse_lazy


@method_decorator(login_required, name="dispatch")
class WellPassportListView(ListView):
    model = WellPassport
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        user_well_passports = request.user.well_passport.all()
        return render(
            request,
            template_name="well_passport/list.html",
            context={"well_passports": user_well_passports, "title": "Well passports"},
        )


@method_decorator(login_required, name="dispatch")
class WellTestView(TemplateView):
    model = WellPassport

    def get(self, request, *args, **kwargs):
        data_to_add = {
            "user": request.user,  # Замените на объект пользователя
            "organization": Organization.objects.get(
                id=1
            ),  # Замените на объект организации
            "project_name": "test_1",
            "well_number": "N_test",
            "ground_lvl": 191.0,
        }
        well_passport = WellPassport.objects.create(**data_to_add)
