import django_tables2 as tables
from django_tables2.utils import A

TEMPLATE = '''
    
'''

class AccessUtilityTable(tables.Table):

    id = tables.Column(
        verbose_name='#'
    )
    name = tables.Column()
    codename = tables.Column()
    actions = tables.TemplateColumn(TEMPLATE)
    class Meta:
        row_attrs = {
            'class': 'bg-white border-b transition duration-300 ease-in-out hover:bg-gray-100 cursor-pointer',
            'id': lambda record: record.pk
        }
        attrs = {
            'class': 'min-w-full mb-8 table-auto ',
            'id': 'access_utility_tbl',
            'thead': {
                'class': 'bg-white border-b'
            },
            'th': {
                'scope': 'col',
                'class': 'text-sm text-gray-900 px-6 py-4 text-left'
            },
            'td': {
                'class': 'text-clip px-6 py-4 text-sm font-medium text-gray-900'
            },
        }
        empty_text = 'There are no access utilities yet.'