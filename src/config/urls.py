from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = (
    [
        path("map_2/", views.MapView_2.as_view(), name="map_2"),
        path("map/points", views.PointsView.as_view(), name="points"),
        path("map/fields", views.FieldsView.as_view(), name="fields"),
        path("map/vzu", views.VZUView.as_view(), name="vzu"),
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
        path("crm/", include("apps.crm.urls"), name="crm_home"),
        path("regime_test/", views.RegimeView.as_view(), name="regime_test"),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
