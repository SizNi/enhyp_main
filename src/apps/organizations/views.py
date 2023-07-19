from django.shortcuts import render, redirect
import uuid
import os
from django.contrib import messages
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from apps.organizations.forms import CreateOrganizationForm, UpdateOrganizationForm
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.organizations.models import Organization


def index(request):
    return HttpResponse("organizations")


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


@method_decorator(login_required, name="dispatch")
class OrganizationCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {}
        form = CreateOrganizationForm()
        context["create_form"] = form
        return render(request, "organizations/create.html", context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = CreateOrganizationForm(request.POST, request.FILES)
        if form.is_valid():
            organization = form.save(commit=False)
            try:
                logo = request.FILES["logo"]
                filename = f"logos/{uuid.uuid4().hex}_{logo.name}"
                filename = default_storage.save(filename, logo)
                organization.logo = filename
            except MultiValueDictKeyError:
                pass
            organization.user = request.user

            organization.save()
            messages.info(request, _("Организация добавлена"))
            return redirect("organizations_mine")
        else:
            context["create_form"] = form
            return render(request, "organizations/create.html", context)


@method_decorator(login_required, name="dispatch")
class OrganizationUpdateView(UpdateView):
    def get(self, request, *args, **kwargs):
        org_id = kwargs.get("pk")
        current_user = request.user
        context = {}
        organization = Organization.objects.get(id=org_id)
        if current_user.id == organization.user_id:
            form = UpdateOrganizationForm(instance=organization)
            context["update_form"] = form
            if organization.logo:
                context["logo"] = organization.logo
            return render(request, "organizations/update.html", context)
        else:
            messages.error(request, _("Сюда не ходите."))
            return redirect("organizations_mine")

    def post(self, request, *args, **kwargs):
        org_id = kwargs.get("pk")
        context = {}
        organization = Organization.objects.get(id=org_id)
        form = UpdateOrganizationForm(
            request.POST, request.FILES, instance=organization
        )
        if form.is_valid():
            organization = form.save(commit=False)
            try:
                logo = request.FILES["logo"]
                filename = f"logos/{uuid.uuid4().hex}_{logo.name}"
                filename = default_storage.save(filename, logo)
                organization.logo = filename
            except MultiValueDictKeyError:
                pass
            organization.user = request.user
            organization.save()
            messages.info(request, _("Информация обновлена"))
            return redirect("home")
        else:
            context["update_form"] = form
            return render(request, "organizations/update.html", context)


@method_decorator(login_required, name="dispatch")
class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = "organizations/delete.html"
    success_url = reverse_lazy("organizations_mine")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):  # не срабатывает (понять почему)
        organization = self.get_object()
        # удаление логотипа
        if organization.logo:
            try:
                logo_path = organization.logo.path
                os.remove(logo_path)
            except Exception as e:
                print(f"Ошибка при удалении логотипа: {e}")
        messages.info(request, _("Организация удалена"))
        return super().delete(request, *args, **kwargs)
