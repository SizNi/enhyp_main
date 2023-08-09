from django.contrib import admin
from django.urls import path, include
from apps.well_section import views

urlpatterns = [
    # path("", views.index, name="well_section_home"),
    path("test/", views.BirdAddView.as_view(), name="well_section_test"),
] 
