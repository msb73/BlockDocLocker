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
class ViewTable(tables.Table):
    name = tables.Column()
    caseNo = tables.Column()
    documentId = tables.Column()
    cid = tables.Column()
    timeStamp = tables.Column()
    documentHash = tables.Column()
    documentType = tables.Column()

# table = PersonTable(data)

