from django.db import models
from django.conf import settings


class Organization(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    org_name = models.CharField(max_length=100)
    inn = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    logo = models.ImageField(upload_to="logos/")

    def __str__(self):
        return self.org_name
