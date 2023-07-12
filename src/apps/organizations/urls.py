from django.contrib import admin
from django.urls import path, include
from apps.organizations import views

urlpatterns = [
    path("", views.index, name="organizations_home"),
    path("create/", views.CreateView.as_view(), name="organization_create"),
]
