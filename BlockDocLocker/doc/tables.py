# tables.py
import django_tables2 as tables
data =  [
    {'name': 'Item 1', 'description': 'Description 1'},
    {'name': 'Item 2', 'description': 'Description 2'},
    {'name': 'Item 3', 'description': 'Description 3'},
]
class SimpleTable(tables.Table):
    name = tables.Column(verbose_name="category",order_by="name")
    description = tables.Column()
    # Add other fields as needed
