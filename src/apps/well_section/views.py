# views.py
from django.views.generic import ListView, TemplateView  # Import TemplateView
from .models import Bird
from .forms import BirdFormSet  # Import the formset
from django.urls import reverse_lazy
from django.shortcuts import redirect


class BirdListView(ListView):
    model = Bird
    template_name = "well_section/test.html"


# View for adding birds
class BirdAddView(TemplateView):
    template_name = "well_section/index.html"

    # Define method to handle GET request
    def get(self, *args, **kwargs):
        # Create an instance of the formset
        formset = BirdFormSet(queryset=Bird.objects.none())
        return self.render_to_response({"bird_formset": formset})

    def post(self, *args, **kwargs):
        formset = BirdFormSet(data=self.request.POST)

        # Check if submitted forms are valid
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy("bird_list"))

        return self.render_to_response({"bird_formset": formset})
