# views.py
from django.views.generic import ListView, TemplateView  # Import TemplateView
from .models import WellSection
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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


# View for adding birds
class WellSectionCreateView(TemplateView):
    template_name = "well_section/create_form.html"
