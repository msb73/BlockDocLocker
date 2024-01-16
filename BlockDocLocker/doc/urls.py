
from django.urls import path

from . import views

urlpatterns = [
    path('',views.home, name="doc-home"),
    path('about/', views.about, name='doc-about'),
    path('upload/', views.upload, name='doc-upload'),
    path('document/', views.document_retrive, name='document'),
    ]
