from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from config.views import TestMailView

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", views.Index.as_view(), name="home"),
        path("users/", include("apps.users.urls"), name="users"),
        path(
            "organizations/", include("apps.organizations.urls"), name="organizations"
        ),
        path("zso/", include("apps.zso.urls"), name="zso"),
        path("well_section/", include("apps.well_section.urls"), name="well_section"),
        path(
            "well_passport/", include("apps.well_passport.urls"), name="well_passport"
        ),
        path(
            "passport_example/",
            views.PassportExampleView.as_view(),
            name="passport_example",
        ),
        ######################
        path("test_mail/", views.TestMailView.as_view(), name="test_mail"),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
