from django.urls import path
from apps.well_passport import views

urlpatterns = [
    path("", views.WellPassportListView.as_view(), name="well_section_list"),
]
