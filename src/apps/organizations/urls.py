from django.contrib import admin
from django.urls import path, include
from apps.organizations import views

urlpatterns = [
    path("", views.index, name="organizations_home"),
    path("my/", views.OrganizationsListView.as_view(), name="organizations_mine"),
    path("create/", views.OrganizationCreateView.as_view(), name="organization_create"),
    path(
        "<int:pk>/update/",
        views.OrganizationUpdateView.as_view(),
        name="organization_update",
    ),
    path(
        "<int:pk>/delete/",
        views.OrganizationDeleteView.as_view(),
        name="organization_delete",
    ),
    path(
        "<int:pk>/update/logo_delete",
        views.OrganizationLogoDeleteView.as_view(),
        name="logo_delete_view",
    ),
    path(
        "verification/<str:verification_code>/",
        views.OrganizationVerificationView.as_view(),
        name="org_email_verification",
    ),
    path(
        "<int:pk>/email_confirmation/",
        views.OrganizationEmailConfirmationView.as_view(),
        name="org_send_email_confirmation",
    ),
]
