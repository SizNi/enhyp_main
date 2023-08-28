from django.shortcuts import render, redirect
import uuid
import os
from django.contrib import messages
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, View
from django.http import HttpResponse, HttpResponseRedirect
from apps.organizations.forms import CreateOrganizationForm, UpdateOrganizationForm
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy, reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.organizations.models import Organization
from apps.organizations.org_confirmation import org_mail_confirmation
from django.utils import timezone
from datetime import timedelta


def index(request):
    return HttpResponse("organizations")


@method_decorator(login_required, name="dispatch")
class OrganizationsListView(TemplateView):
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
            try:
                # функция отправки почты для верифицкации
                org_mail_confirmation(organization)
                messages.info(
                    request,
                    _("Организация создана, подтвердите электронную почту организации"),
                )
            except Exception as e:
                messages.error(
                    request,
                    _(
                        "Произошла ошибка при отправке письма с подтверждением. Пожалуйста, свяжитесь с администратором."
                    ),
                )
                print(f"Ошибка отправки почты: {e}")
            return redirect("organizations_mine")
        else:
            context["create_form"] = form
            return render(request, "organizations/create.html", context)


@method_decorator(login_required, name="dispatch")
class OrganizationUpdateView(UpdateView):
    template_name = "organizations/update.html"

    def get(self, request, *args, **kwargs):
        org_id = kwargs.get("pk")
        try:
            organization = Organization.objects.get(id=org_id, user=request.user)
        except Organization.DoesNotExist:
            messages.error(request, "Вы не можете редактировать эту организацию.")
            return redirect("organizations_mine")
        form = UpdateOrganizationForm(instance=organization)
        context = {
            "update_form": form,
            "id": org_id,
            "email_status": organization.confirmed,
        }
        if organization.logo:
            context["logo"] = organization.logo
        return render(request, "organizations/update.html", context)

    def post(self, request, *args, **kwargs):
        org_id = kwargs.get("pk")
        organization = Organization.objects.get(id=org_id)
        old_email = organization.email
        form = UpdateOrganizationForm(
            request.POST, request.FILES, instance=organization
        )
        print(organization.logo)
        if form.is_valid():
            organization = form.save(commit=False)
            new_email = organization.email
            # лишнее но именует файл логотипа. переделать
            # форма удаляет старое в любом случае, а если нового нет - то не перезаписывает. Поправить
            try:
                logo = request.FILES["logo"]
                # filename = f"logos/{uuid.uuid4().hex}_{logo.name}"
                filename = f"logos/{logo.name}"
                filename = default_storage.save(filename, logo)
                organization.logo = filename
            except MultiValueDictKeyError:
                pass
            organization.save()
            if new_email != old_email:
                try:
                    # функция отправки почты для верифицкации
                    org_mail_confirmation(organization)
                    messages.info(
                        request,
                        _(
                            "Информация обновлена, подтвердите электронную почту организации"
                        ),
                    )
                except Exception as e:
                    messages.error(
                        request,
                        _(
                            "Произошла ошибка при отправке письма с подтверждением. Пожалуйста, свяжитесь с администратором."
                        ),
                    )
                    print(f"Ошибка отправки почты: {e}")
            else:
                messages.info(
                    request,
                    _("Информация обновлена"),
                )
            return redirect("organizations_mine")
        else:
            context = {"update_form": form}
            return render(request, "organizations/update.html", context)


######################################################################## тестовый вью
@method_decorator(login_required, name="dispatch")
class TestOrganizationUpdateView(View):
    template_name = "organizations/update.html"

    def get(self, request, *args, **kwargs):
        org_id = kwargs.get("pk")
        try:
            organization = Organization.objects.get(id=org_id, user=request.user)
        except Organization.DoesNotExist:
            messages.error(request, "Вы не можете редактировать эту организацию.")
            return redirect("organizations_mine")

        form = UpdateOrganizationForm(instance=organization)
        return render(
            request,
            self.template_name,
            {"update_form": form, "organization": organization},
        )

    def post(self, request, *args, **kwargs):
        org_id = kwargs.get("pk")
        organization = Organization.objects.get(id=org_id, user=request.user)
        form = UpdateOrganizationForm(
            request.POST, request.FILES, instance=organization
        )
        if form.is_valid():
            organization = form.save(commit=False)
            organization.user = request.user
            organization.save()
            messages.success(request, "Данные организации успешно обновлены.")
            return redirect("organizations_mine")
        else:
            messages.error(request, "Исправьте ошибки в форме.")

        return render(
            request, self.template_name, {"form": form, "organization": organization}
        )


######################################################################## тестовый вью


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


@method_decorator(login_required, name="dispatch")
class OrganizationLogoDeleteView(View):
    def get(self, request, *args, **kwargs):
        org_id = kwargs.get("pk")
        current_user = request.user
        context = {}
        organization = Organization.objects.get(id=org_id)
        if current_user.id == organization.user_id:
            context["logo"] = organization.logo
            return render(request, "organizations/delete_logo.html", context)
        else:
            messages.error(request, _("Сюда не ходите."))
            return redirect("organizations_mine")

    def post(self, request, *args, **kwargs):
        org_id = kwargs.get("pk")
        current_user = request.user
        organization = Organization.objects.get(id=org_id)
        if current_user.id == organization.user_id:
            # Удаление логотипа из базы данных и файловой системы
            try:
                logo_path = organization.logo.path
                os.remove(logo_path)
                organization.logo.delete()
                messages.info(request, _("Логотип удален"))
            except Exception as e:
                print(f"Ошибка при удалении логотипа: {e}")
                organization.logo.delete()
        return HttpResponseRedirect(reverse("organization_update", args=[org_id]))


@method_decorator(login_required, name="dispatch")
class OrganizationVerificationView(TemplateView):
    def get(self, request, *args, **kwargs):
        verification_code = kwargs.get("verification_code")
        try:
            organization = Organization.objects.get(confirmation_code=verification_code)
        except:
            messages.error(
                request,
                _(
                    "Ссылка для подтверждения не найдена, обратитесь к администратору или запросите ее повторно"
                ),
            )
            return redirect("organization_update")
        expiration_time = organization.confirmation_code_dt + timedelta(days=7)
        current_time = timezone.now()
        context = {}
        # устанавливаем срок действия ссылки
        if current_time > expiration_time:
            messages.error(
                request,
                _(
                    "Истек срок действия ссылки. Запросите новую в своем профиле"
                ),  # новую надо реализовать
            )
            return redirect("organization_update")
        # сраниваем коды верификации
        if organization.user == request.user:
            organization.confirmed = True
            organization.confirmation_code = ""
            organization.save()
            context["email"] = organization.email
            context["name"] = organization.org_name
            messages.success(request, _("Почта подтверждена!"))
            return render(request, "organizations/mail_verification.html", context)
        else:
            messages.error(
                request, _("Верификация не удалась, обратитесь к администратору")
            )
            return redirect("home")


@method_decorator(login_required, name="dispatch")
class OrganizationEmailConfirmationView(TemplateView):
    def get(self, request, *args, **kwargs):
        org_id = kwargs.get("pk")
        organization = Organization.objects.get(id=org_id)
        context = {}
        if organization.user == request.user:
            context["name"] = organization.org_name
            context["email"] = organization.email
            try:
                # функция отправки почты для верифицкации
                org_mail_confirmation(organization)
                messages.info(
                    request,
                    _("Письмо с подтверждением отправлено на почту"),
                )
            except Exception as e:
                messages.error(
                    request,
                    _(
                        "Произошла ошибка при отправке письма с подтверждением. Пожалуйста, свяжитесь с администратором."
                    ),
                )
                print(f"Ошибка отправки почты: {e}")
            return render(
                request, "organizations/send_email_confirmation.html", context
            )
        else:
            messages.error(
                request,
                _("У вас нет прав для изменения организации другого пользователя."),
            )
            return redirect("home")
