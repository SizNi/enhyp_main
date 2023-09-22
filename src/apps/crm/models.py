from django.db import models
from django.conf import settings
from apps.organizations.models import Organization


class Crm(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="crm", on_delete=models.CASCADE
    )
    organization = models.ForeignKey(
        Organization, related_name="crm", on_delete=models.CASCADE
    )
    project_name = models.CharField(max_length=200)
    project_status = models.BooleanField(default=False)
    contract_file = models.FileField(upload_to="crm/contracts", null=True)
    note = models.CharField(max_length=200, null=True)
    work_list = models.CharField(max_length=200, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)


class License(models.Model):
    crm = models.OneToOneField(Crm, on_delete=models.CASCADE, related_name="license")
    license_name = models.CharField(max_length=12)
    license_status = models.BooleanField(default=False)
    license_file = models.FileField(upload_to="crm/license", null=True)
    note = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    second_license_file = models.FileField(upload_to="crm/license", null=True)
    second_note = models.CharField(max_length=200, null=True)
    second_created_at = models.DateTimeField(blank=True, null=True)
    second_end_at = models.DateTimeField(blank=True, null=True)


class Gin(models.Model):
    crm = models.OneToOneField(Crm, on_delete=models.CASCADE, related_name="gin")
    gin_name = models.CharField(max_length=12)
    gin_status = models.BooleanField(default=False)
    gin_file = models.FileField(upload_to="crm/gin/project", null=True)
    eks_file = models.FileField(upload_to="crm/gin/eks", null=True)
    note = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)


class Zso(models.Model):
    crm = models.OneToOneField(Crm, on_delete=models.CASCADE, related_name="zso")
    zso_name = models.CharField(max_length=12)
    zso_status = models.BooleanField(default=False)
    zso_file = models.FileField(upload_to="crm/zso/project", null=True)
    eks_file = models.FileField(upload_to="crm/zso/eks", null=True)
    sez_file = models.FileField(upload_to="crm/zso/sez", null=True)
    note = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)


class Pkk(models.Model):
    crm = models.OneToOneField(Crm, on_delete=models.CASCADE, related_name="pkk")
    pkk_name = models.CharField(max_length=12)
    pkk_status = models.BooleanField(default=False)
    pkk_file = models.FileField(upload_to="crm/pkk/project", null=True)
    eks_file = models.FileField(upload_to="crm/pkk/eks", null=True)
    sez_file = models.FileField(upload_to="crm/pkk/sez", null=True)
    note = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)


# оценка запасов
class Resources(models.Model):
    crm = models.OneToOneField(Crm, on_delete=models.CASCADE, related_name="resources")
    resources_name = models.CharField(max_length=12)
    resources_status = models.BooleanField(default=False)
    resources_file = models.FileField(upload_to="crm/resources/project", null=True)
    protocol_file = models.FileField(upload_to="crm/resources/protocol", null=True)
    # план подсчета запасов с печатью и подписью ГКЗ/ТКЗ
    plan_file = models.FileField(upload_to="crm/resources/plan", null=True)
    note = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)


# проект разработки месторождения
class Development(models.Model):
    crm = models.OneToOneField(
        Crm, on_delete=models.CASCADE, related_name="development"
    )
    development_name = models.CharField(max_length=12)
    development_status = models.BooleanField(default=False)
    development_file = models.FileField(upload_to="crm/development/project", null=True)
    eks_file = models.FileField(upload_to="crm/development/eks", null=True)
    note = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
