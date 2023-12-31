from django.contrib import admin
from django.urls import path, include
from apps.zso import views

urlpatterns = [
    path("", views.ZsoListView.as_view(), name="zso_list"),
    path("create/", views.ZsoFirstCreateView.as_view(), name="zso_create"),
    path(
        "<int:pk>/create_second/",
        views.ZsoSecondCreateView.as_view(),
        name="zso_create_second",
    ),
    path("<int:pk>/watch/", views.ZsoWatchView.as_view(), name="zso_watch"),
    path(
        "<int:pk>/delete",
        views.ZsoDeleteView.as_view(),
        name="zso_delete",
    ),
]
