from django.db import models
from django.conf import settings
from apps.organizations.models import Organization
from django.core.exceptions import ValidationError


def validate_file_size(value):
    limit = 10 * 1024 * 1024  # 10 MB
    if value.size > limit:
        raise ValidationError(f"Размер файла не должен превышать 10 мегабайт.")


class WellPassport(models.Model):
    # внутреняя информация
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="well_passport", on_delete=models.CASCADE
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    project_name = models.CharField(max_length=100, blank=True)
    # основные поля
    well_number = models.CharField(max_length=100, blank=True)
    passport_type = models.CharField(max_length=100, blank=True)
    republic = models.CharField(max_length=100, null=True)
    region = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=200, null=True)
    well_owner = models.CharField(max_length=200, null=True)
    mailing_adress = models.CharField(max_length=200, null=True)
    NL = models.CharField(max_length=40, null=True)
    SL = models.CharField(max_length=40, null=True)
    ground_lvl = models.FloatField(null=True)
    well_type = models.CharField(max_length=200, null=True)
    well_purpose = models.CharField(max_length=200, null=True)
    drilling_method = models.CharField(max_length=200, null=True)
    rig = models.CharField(max_length=200, null=True)
    project_owner = models.CharField(max_length=200, null=True)
    drilling_company = models.CharField(max_length=200, null=True)
    start = models.DateField(null=True)
    end = models.DateField(null=True)
    finishing = models.DateField(null=True)
    # дополнительная информация по скважине
    pump_power = models.FloatField(null=True)
    pump_column = models.FloatField(null=True)
    debit = models.FloatField(null=True)
    # общие данные, требующие сериализации
    gis_data = models.CharField(max_length=400, null=True)
    ofr_data = models.CharField(max_length=400, null=True)
    # это должно присосаться к well_data['cementation'] и тоже сериализовать
    cementation_data = models.CharField(max_length=400, null=True)
    # дополнительные файлы
    gis = models.FileField(
        upload_to="well_passport/gis/", validators=[validate_file_size], null=True
    )
    analyses = models.FileField(
        upload_to="well_passport/analyses/", validators=[validate_file_size], null=True
    )
    acts = models.FileField(
        upload_to="well_passport/acts/", validators=[validate_file_size], null=True
    )
    sro = models.FileField(
        upload_to="well_passport/sro/", validators=[validate_file_size], null=True
    )
    others_apps_name = models.CharField(max_length=200, null=True)
    others_apps = models.FileField(
        upload_to="well_passport/others/", validators=[validate_file_size], null=True
    )
    # связь с разрезом
    well_section = models.OneToOneField(
        "well_section.WellSection",
        on_delete=models.CASCADE,
        related_name="passport",
        null=True,
    )
