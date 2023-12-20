
from django.urls import path

from . import views

urlpatterns = [
    path('',views.first, name="doc-home"),
    path('about/', views.about, name='doc-about'),
    path('uploadDocument/', views.uploadDocuments.as_view(), name='uploadDocument'),
    path('documents/', views.ViewDocuments.as_view(), name = "viewDocuments"),
    # path('my-table/', views.SimpleTableView.as_view(), name='my_table'),
    path('addusers/', views.AddUser.as_view(), name = "addUsers"),
    # path('requests', views.CheckRequests.as_view(), name = "checkRequests")
    path('checkRequests/', views.CSRequestView.as_view(), name='checkRequests'),

    ]
