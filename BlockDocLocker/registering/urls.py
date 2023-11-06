from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as views_log
from . import views



urlpatterns = [
    path('',views.register, name="register"),
    path('profile/',views.profile, name="profile"),
    path('login/',views_log.LoginView.as_view(template_name='registering/login.html'), name='login'),
    path('logout/',views_log.LogoutView.as_view(template_name='registering/logout.html'), name='logout'),
    ]

