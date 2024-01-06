
from django.urls import path

from . import views

urlpatterns = [
    path('',views.home, name="doc-home"),
    # path('about/', views.about, name='doc-about'),
    path('uploadDocument/', views.uploadDocuments.as_view(), name='uploadDocument'),
    path('documents/', views.ViewDocuments.as_view(), name = "viewDocuments"),
    path('addUsers/', views.AddUser.as_view(), name = "addUsers"),
    # path('checkRequests/', views.CSARequestView.as_view(), name='allUsers'),
    path('checkRequests/', views.SendRequestView.as_view(), name='allDocuments'),
    # path('checkRequests/', views.CSARequestView.as_view(), name='allCases'),
    path('Requests/', views.ApproveRequests.as_view(), name='checkApprovals'),

    ]
# allCases -> {'0': [['102', 'Ginson vs Yogi']], '1': ['0x28379662D72D25660af75b7F71D645303713C1cf', '0xbd5E32346805A87aaBD814D495404F6c04eB89a9'], '2': ['owner', 'Milind']}
# allUsers -> {'0': ['0x28379662D72D25660af75b7F71D645303713C1cf', '0xbd5E32346805A87aaBD814D495404F6c04eB89a9'], '1': ['owner', 'Milind']}
# allDocuments -> {'0': ['1', '2', '0'], '1': ['case201', 'case101', ''], '2': ['0', '2'], '3': ['owner', 'Milind']}
# viewDocuemnts -> [['case101-1', '101', '101000000003', 'ASEiC', '1704118031', 'text', '0x0000000000000000000000000000000000000000', 'Nothing']]
# checkApprovals -> [['4', '0xbd5E32346805A87aaBD814D495404F6c04eB89a9', 'Sagar', '101000000003', 'case101-1', '1704204673', '17999999'], ['5', '0xbd5E32346805A87aaBD814D495404F6c04eB89a9', 'Sagar', '102000000002', 'case102-2', '1704204673', '17999999']]
# checkRequests -> {'0': ['101000000003', '102000000002'], '1': ['case101-1', 'case102-2']}