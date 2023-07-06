from django.contrib import admin
from django.urls import path, include
from apps.users import views

urlpatterns = [
    path('', views.index, name='users_home'),
    path('login/', views.LoginView.as_view(), name='user_login'),
    path('registration/', views.CreateView.as_view(), name='user_create'),
]
