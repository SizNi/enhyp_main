from django.urls import path
from apps.well_passport import views

urlpatterns = [
    path("", views.WellPassportListView.as_view(), name="well_passport_list"),
    path("test/", views.WellTestView.as_view(), name="well_passport_test"),
]
