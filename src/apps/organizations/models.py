from django.db import models
from django.conf import settings


class Organization(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="organizations", on_delete=models.CASCADE
    )
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

    def __str__(self):
        return self.org_name
