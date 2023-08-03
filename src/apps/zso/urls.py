from django.contrib import admin
from django.urls import path, include
from apps.zso import views

urlpatterns = [
    path("", views.index, name="zso_home"),
    path("create/", views.ZsoFirstCreateView.as_view(), name="zso_create"),
    path(
        "<int:pk>/create_second/",
        views.ZsoSecondCreateView.as_view(),
        name="zso_create_second",
    ),
]