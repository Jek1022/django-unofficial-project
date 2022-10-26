import django_tables2 as tables
from django_tables2.utils import A

class DeptTable(tables.Table):
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
    description = tables.Column(attrs={
        'th': {
            'scope': 'col',
            'class': 'text-sm font-medium text-gray-900 px-6 py-4 text-left'
        }
    })
    delete = tables.LinkColumn('delete_department', args=[A('pk')], orderable=False, empty_values=(), text='Delete', attrs={
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
            'class': 'min-w-full mb-8',
            'id': 'department',
            'thead': {
                'class': 'bg-white border-b'
            },
            'td': {
                'class': 'px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900'
            },
        }