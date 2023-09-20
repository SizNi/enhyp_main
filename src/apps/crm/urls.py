from django.contrib import admin
from django.urls import path, include
from apps.crm import views


urlpatterns = [
    path("", views.index, name="crm_home"),
    path("upload/", views.upload_file, name="upload_file"),
]
