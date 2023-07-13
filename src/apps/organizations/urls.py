from django.contrib import admin
from django.urls import path, include
from apps.organizations import views

urlpatterns = [
    path("", views.index, name="organizations_home"),
    path("my/", views.MyOrganizationsView.as_view(), name="organizations_mine"),
    path("create/", views.CreateView.as_view(), name="organization_create"),
]
