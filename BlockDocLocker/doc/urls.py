
from django.urls import path

from . import views

urlpatterns = [
    path('',views.home, name="doc-home"),
    # path('about/', views.about, name='doc-about'),
    path('uploadDocument/', views.uploadDocuments.as_view(), name='uploadDocument'),
    path('documents/', views.ViewDocuments.as_view(), name = "viewDocuments"),
    path('addUsers/', views.AddUser.as_view(), name = "addUsers"),
    path('checkRequests/', views.CSARequestView.as_view(), name='checkRequests'),
    path('checkRequests/', views.CSARequestView.as_view(), name='allDocuments'),
    path('approveRequests/', views.CSARequestView.as_view(), name='checkRequests'),
    path('checkRequests/', views.CSARequestView.as_view(), name='checkApprovals'),
    path('Requests/', views.Requests.as_view(), name='checkApprovals'),
    

    ]
