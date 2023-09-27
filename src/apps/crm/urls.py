from django.contrib import admin
from django.urls import path, include
from apps.crm import views


urlpatterns = [
    path("", views.IndexView.as_view(), name="crm_home"),
]
