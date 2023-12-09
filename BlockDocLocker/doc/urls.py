
from django.urls import path

from . import views

urlpatterns = [
    path('',views.first, name="doc-home"),
    path('about/', views.about, name='doc-about'),
    path('upload/', views.FileFieldFormView.as_view(), name='doc-upload'),
    path('documents/', views.viewDocuments, name = "viewDocuments")
    ]
