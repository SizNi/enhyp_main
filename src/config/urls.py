from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = (
    [
        path("map/", views.MapView.as_view(), name="map"),
        path("map_2/", views.MapView2.as_view(), name="map_2"),
        path("map_2/points.geojson", views.MapView2Points.as_view(), name="map_2_points"),
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
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
