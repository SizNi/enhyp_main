from django.contrib import admin
from django.urls import path, include
from apps.users import views

urlpatterns = [
    path("", views.index, name="users_home"),
    path("login/", views.LoginView.as_view(), name="user_login"),
    path("registration/", views.CreateView.as_view(), name="user_create"),
    path("logout/", views.LogoutView.as_view(), name="user_logout"),
    path("<int:pk>/update/", views.UserUpdateView.as_view(), name="user_update"),
    path(
        "verification/<str:verification_code>/",
        views.UserVerificationView.as_view(),
        name="email_verification",
    ),
    path(
        "<int:pk>/email_confirmation/",
        views.UserEmailConfirmationView.as_view(),
        name="send_email_confirmation",
    ),
    path("recovery/", views.UserRecoveryView.as_view(), name="user_recovery"),
    path(
        "recovery/<str:recovery_code>/",
        views.UserRecoverySecondView.as_view(),
        name="user_recovery_url",
    ),
]
