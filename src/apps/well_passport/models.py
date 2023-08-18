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
    republic = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    well_owner = models.CharField(max_length=200)
    mailing_adress = models.CharField(max_length=200)
    NL = models.CharField(max_length=40)
    SL = models.CharField(max_length=40)
    ground_lvl = models.FloatField()
    well_type = models.CharField(max_length=200)
    well_purpose = models.CharField(max_length=200)
    drilling_method = models.CharField(max_length=200)
    rig = models.CharField(max_length=200)
    project_owner = models.CharField(max_length=200)
    drilling_company = models.CharField(max_length=200)
    start = models.DateField()
    end = models.DateField()
    finishing = models.DateField()
    # дополнительная информация по скважине
    pump_power = models.FloatField()
    pump_column = models.FloatField()
    debit = models.FloatField()
    # общие данные, требующие сериализации
    gis_data = models.CharField(max_length=400)
    ofr_data = models.CharField(max_length=400)
    # это должно присосаться к well_data['cementation'] и тоже сериализовать
    cementation_data = models.CharField(max_length=400)
    # дополнительные файлы
    gis = models.FileField(
        upload_to="well_passport/gis/", validators=[validate_file_size]
    )
    analyses = models.FileField(
        upload_to="well_passport/analyses/", validators=[validate_file_size]
    )
    acts = models.FileField(
        upload_to="well_passport/acts/", validators=[validate_file_size]
    )
    sro = models.FileField(
        upload_to="well_passport/sro/", validators=[validate_file_size]
    )
    others_apps_name = models.CharField(max_length=200)
    others_apps = models.FileField(
        upload_to="well_passport/others/", validators=[validate_file_size]
    )
    # связь с разрезом
    well_section = models.OneToOneField(
        "well_section.WellSection",
        on_delete=models.CASCADE,
        related_name="passport",
    )
