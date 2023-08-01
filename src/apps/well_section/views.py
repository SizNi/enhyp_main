from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name="dispatch")
class IndexWellView(TemplateView):

    def get(self, request, *args, **kwargs):
        user_organizations = request.user.organizations.all()
        return render(
            request,
            template_name="well_section/index.html",
            context={"organizations": user_organizations, "title": "Organizations"},
        )