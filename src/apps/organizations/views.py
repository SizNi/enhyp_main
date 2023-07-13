from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from apps.organizations.forms import CreateOrganizationForm
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.organizations.models import Organization


def index(request):
    return HttpResponse("organizations")


@method_decorator(login_required, name="dispatch")
class CreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {}
        form = CreateOrganizationForm()
        context["create_form"] = form
        return render(request, "organizations/create.html", context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = CreateOrganizationForm(request.POST)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.user = request.user
            organization.save()
            messages.info(request, _("Организация добавлена"))
            return redirect("home")
        else:
            context["create_form"] = form
            return render(request, "organizations/create.html", context)


@method_decorator(login_required, name="dispatch")
class MyOrganizationsView(TemplateView):
    template_name = "organizations/list.html"

    def get(self, request, *args, **kwargs):
        user_organizations = request.user.organizations.all()
        return render(
            request,
            template_name="organizations/list.html",
            context={"organizations": user_organizations, "title": "Organizations"},
        )
