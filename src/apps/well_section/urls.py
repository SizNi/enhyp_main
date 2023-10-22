from django.urls import path
from apps.well_section import views

urlpatterns = [
    path("", views.WellSectionListView.as_view(), name="well_section_list"),
    path("create/", views.WellSectionCreateView.as_view(), name="well_section_create"),
    path(
        "create_test/",
        views.WellSectionCreateView_2.as_view(),
        name="well_section_create_2",
    ),
    path(
        "<int:pk>/", views.WellSectionResultView.as_view(), name="well_section_result"
    ),
    path(
        "<int:pk>/delete",
        views.WellSectionDeleteView.as_view(),
        name="well_section_delete",
    ),
]
