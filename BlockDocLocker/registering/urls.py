from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as views_log
from . import views



urlpatterns = [
    path('',views.register, name='register'),

    ]

