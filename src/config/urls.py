from django.contrib import admin
from django.urls import path, include
from config import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.Index.as_view(), name="home"),
    path("users/", include("apps.users.urls"), name="users"),
    path("organizations/", include("apps.organizations.urls"), name="organizations"),
]
