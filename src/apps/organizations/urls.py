from django.contrib import admin
from django.urls import path, include
from apps.organizations import views

urlpatterns = [
    path("", views.index, name="organizations_home"),
    path("my/", views.MyOrganizationsView.as_view(), name="organizations_mine"),
    path("create/", views.OrganizationCreateView.as_view(), name="organization_create"),
    path("<int:pk>/update/", views.OrganizationUpdateView.as_view(), name="organization_update"),
    path("<int:pk>/delete/", views.OrganizationDeleteView.as_view(), name="organization_delete"),
]
