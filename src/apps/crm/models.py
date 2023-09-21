from django.db import models
from django.conf import settings
from apps.organizations.models import Organization


class Crm(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="crm", on_delete=models.CASCADE
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    org_name = models.CharField(max_length=100)
    inn = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    ceo_name = models.CharField(max_length=25)
    originator_position = models.CharField(max_length=25)
    originator_name = models.CharField(max_length=25)
    logo = models.ImageField(upload_to="logos/")
    confirmed = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=20, blank=True, null=True)
    confirmation_code_dt = models.DateTimeField(blank=True, null=True)
