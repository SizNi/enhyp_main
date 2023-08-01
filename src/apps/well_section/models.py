from django.db import models
from django.conf import settings


class Well_section(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="well_user", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    layers_count = models.IntegerField()
    columns_count = models.IntegerField()
    address = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    logo = models.ImageField(upload_to="logos/")

    def __str__(self):
        return self.org_name
