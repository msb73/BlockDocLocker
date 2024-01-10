
from django.urls import path

from . import views

urlpatterns = [
    path('',views.home, name="doc-home"),
    path('updocument/', views.uploadDocuments.as_view(), name='uploadDocuments'),
    path('documents/', views.ViewDocuments.as_view(), name = "viewDocuments"),
    path('addusers/', views.AddUser.as_view(), name = "addUsers"),
    path('checkrequests/', views.SendRequestView.as_view(), name='sendRequests'),
    path('approvals/', views.ApproveRequests.as_view(), name='checkApprovals'),
    path('addcases/', views.AddCases.as_view(), name='addCases'), 
    path('removeusers/', views.RemoveUsers.as_view(), name='removeUsers'),
    path('changeincharge/', views.ChangeIncharge.as_view(), name='changeIncharge'), 
    

    ]
# allCases -> {'0': [['102', 'Ginson vs Yogi']], '1': ['0x28379662D72D25660af75b7F71D645303713C1cf', '0xbd5E32346805A87aaBD814D495404F6c04eB89a9'], '2': ['owner', 'Milind']}
# allUsers -> {'0': ['0x28379662D72D25660af75b7F71D645303713C1cf', '0xbd5E32346805A87aaBD814D495404F6c04eB89a9'], '1': ['owner', 'Milind']}
# allDocuments -> {'0': ['1', '2', '0'], '1': ['case201', 'case101', ''], '2': ['0', '2'], '3': ['owner', 'Milind']}
# viewDocuemnts -> [['case101-1', '101', '101000000003', 'ASEiC', '1704118031', 'text', '0x0000000000000000000000000000000000000000', 'Nothing']]
# checkApprovals -> [['4', '0xbd5E32346805A87aaBD814D495404F6c04eB89a9', 'Sagar', '101000000003', 'case101-1', '1704204673', '17999999'], ['5', '0xbd5E32346805A87aaBD814D495404F6c04eB89a9', 'Sagar', '102000000002', 'case102-2', '1704204673', '17999999']]
# checkRequests -> {'0': ['101000000003', '102000000002'], '1': ['case101-1', 'case102-2']}