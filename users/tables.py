import django_tables2 as tables
from django_tables2.utils import A

from rhoel_unofficial_project.views import department
class EmployeeTable(tables.Table):

    id = tables.Column(attrs={
        'th': {
            'scope': 'col',
            'class': 'text-sm font-medium text-gray-900 px-6 py-4 text-left'
        }
    })
    name = tables.Column(attrs={
        'th': {
            'scope': 'col',
            'class': 'text-sm font-medium text-gray-900 px-6 py-4 text-left'
        }
    })
    department = tables.Column(attrs={
        'th': {
            'scope': 'col',
            'class': 'text-sm font-medium text-gray-900 px-6 py-4 text-left'
        }
    })
    action = tables.LinkColumn('user_delete_employee', args=[A('pk')], orderable=False, empty_values=(), text='Delete', 
        attrs = {
            'a': {'class': 'text-sm'},
            'th': {
                'scope': 'col',
                'class': 'text-sm font-medium text-gray-900 px-6 py-4 text-left'
        }
    })
    class Meta:
        row_attrs = {
            'class': 'bg-white border-b transition duration-300 ease-in-out hover:bg-gray-100 cursor-pointer',
            'id': lambda record: record.pk
        }
        attrs = {
            'class': 'min-w-full mb-8 table-auto',
            'id': 'employee_tbl',
            'thead': {
                'class': 'bg-white border-b'
            },
            'td': {
                'class': 'px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900'
            },
        }
        empty_text = 'There are no employees yet.'
        