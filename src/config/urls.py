from django.contrib import admin
from django.urls import path, include
from config import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.Index.as_view(), name="home"),
    path("users/", include("apps.users.urls"), name="users"),
    path("organizations/", include("apps.organizations.urls"), name="organizations"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
