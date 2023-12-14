
from django.urls import path

from . import views

urlpatterns = [
    path('',views.first, name="doc-home"),
    path('about/', views.about, name='doc-about'),
    path('upload/', views.uploadDocuments.as_view(), name='doc-upload'),
    path('documents/', views.ViewDocuments.as_view(), name = "viewDocuments"),
    # path('my-table/', views.SimpleTableView.as_view(), name='my_table'),

    ]
