from django.contrib import admin
from django.urls import path, include
from apps.well_section import views

urlpatterns = [
    path("", views.WellSectionListView.as_view(), name="well_section_list"),
    path("create/", views.WellSectionCreateView.as_view(), name="well_section_create"),
]
