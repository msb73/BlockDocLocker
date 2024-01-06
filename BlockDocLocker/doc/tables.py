# tables.py
import django_tables2 as tables
# data =  [
#     {'name': 'Item 1', 'description': 'Description 1'},
#     {'name': 'Item 2', 'description': 'Description 2'},
#     {'name': 'Item 3', 'description': 'Description 3'},
# ]
# data = [
#     {"name": "Bradley"},
#     {"name": "Stevi"}, = 
# ]
from .names import *

class ViewTable(tables.Table):
    for i in tableViewDocs: 
        locals()[i] = tables.Column()
        
# table = PersonTable(data)
class CheckApprovalsTable(tables.Table):
    for i in tableCheckApprovals:
        locals()[i] = tables.Column()

class CheckRequestsTable(tables.Table):
    for i in tableCheckRequests:
        locals()[i] = tables.Column()
    
class AllUsers(tables.Table): 
    for i in tableAllUsers:
        locals()[i] = tables.Column()
