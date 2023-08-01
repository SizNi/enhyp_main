from django.contrib import admin
from django.urls import path, include
from apps.zso import views

urlpatterns = [
    path("", views.index, name="well_section_home"),
]
