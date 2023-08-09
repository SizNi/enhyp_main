from django.db import models
from django.conf import settings


class WellSection(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="well_section", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=30)
    layers = models.TextField()
    well_data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
