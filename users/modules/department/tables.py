import django_tables2 as tables
from django_tables2.utils import A

TEMPLATE = '''
    <div class="grid grid-cols-3 divide-x-4">
        <div class="divide-x-2">
            <a href="{% url 'view_department' record.id %}" class="text-sm text-blue-700" title="View Department">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m5.231 13.481L15 17.25m-4.5-15H5.625c-.621 0-1.125.504-1.125 1.125v16.5c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9zm3.75 11.625a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
                </svg>
            </a>
        </div>
        <div class="divide-x-2">
            <a href="{% url 'delete_department' record.id %}" class="text-sm text-red-700" title="Delete Department">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                </svg>
            </a>
        </div>
        <div class="text-sm text-yellow-700 divide-x-2" title="Update Department" id="edit_department">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
            </svg>
        </div>
    </div>
'''

class DeptTable(tables.Table):

    id = tables.Column(
        verbose_name='#'
    )
    name = tables.Column()
    description = tables.Column()
    actions = tables.TemplateColumn(TEMPLATE)
    class Meta:
        row_attrs = {
            'class': 'bg-white border-b transition duration-300 ease-in-out hover:bg-gray-100 cursor-pointer',
            'id': lambda record: record.pk
        }
        attrs = {
            'class': 'min-w-full mb-8 table-auto ',
            'id': 'department_tbl',
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
        empty_text = 'There are no departments yet.'