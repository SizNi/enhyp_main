from django.db import models
from django.conf import settings


class Zso(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="zso", on_delete=models.CASCADE
    )
    project_name = models.CharField(max_length=30, blank=True, null=True)
    k_f_min = models.FloatField()
    k_f_max = models.FloatField()
    i_min = models.FloatField()
    i_max = models.FloatField()
    alfa_min = models.FloatField()
    alfa_max = models.FloatField()
    m_min = models.FloatField()
    m_max = models.FloatField()
    por_min = models.FloatField()
    por_max = models.FloatField()
    well_numbers = models.IntegerField()
    debits = models.TextField()
    n_x_skv = models.TextField()
    n_y_skv = models.TextField()
    iteration_count = models.IntegerField()
    b_size = models.FloatField()
    n_x = models.IntegerField()
    n_y = models.IntegerField()
    d_t = models.FloatField()
    n_step = models.IntegerField()
    type = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
