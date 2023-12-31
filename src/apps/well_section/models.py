from django.db import models
from django.conf import settings
import json


class WellSection(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="well_section", on_delete=models.CASCADE
    )
    name = models.TextField()
    layers = models.TextField()
    well_data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_deserialized_name(self):
        try:
            return json.loads(self.name)
        except json.JSONDecodeError:
            return self.name
