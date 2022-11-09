from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import Permission
from django.contrib import messages
from django.shortcuts import redirect
from django.template.loader import render_to_string
from .tables import EmployeeTable
from .forms import EmployeeForm
from .models import Employee
from .file_process import html_to_pdf 
import csv, xlwt

def user_permission(request, action) -> bool:
    permission = Permission.objects.filter(user=request.user, codename=action)
    return permission

# index page
def employee(request):
    form = EmployeeForm
    table = EmployeeTable(Employee.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=5)
    return render(request, 'user/pages/modules/employee/employee.html', {'form': form, 'table': table})

def search(request):
    permissioned = user_permission(request, 'search_employee')
    if permissioned:
        keyword = request.GET.get('q')
        if keyword:
            try:
                results = EmployeeTable(Employee.objects.filter(Q(name__icontains=keyword)))
                if results:
                    table = results.paginate(page=request.GET.get('page', 1), per_page=5)
                else:
                    table = "not found."
                form = EmployeeForm
                return render(request, 'user/pages/modules/employee/employee.html', {'table': table, 'form': form})
            except:
                messages.error(request, "There was a problem on your search.")
        else:
            messages.info(request, "Please enter your search keyword.")
    else:
        messages.info(request, "You don’t have permission to search employee.")
    return redirect('/employee/')

def create_employee(request):
    if request.method == 'POST':
        permissioned = user_permission(request, 'add_employee')
        if permissioned:
            form = EmployeeForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                messages.warning(request, form.errors.as_text())
        else:
            messages.info(request, "You don’t have permission to add employee.")
    return redirect('/employee/')

def view_employee(request, id):
    permissioned = user_permission(request, 'view_employee')
    if permissioned:
        employee = Employee.objects.get(id=id)
        return render(request, 'user/pages/modules/employee/view_employee.html', {'employee': employee})
    else:
        messages.info(request, "You don’t have permission to view employee.")
        return redirect('/employee/')

def update_employee(request, id):
    if not request.GET.get('page'):
        permissioned = user_permission(request, 'change_employee')
        if permissioned:
            name = request.POST['name']
            department = request.POST['department']
            Employee.objects.filter(id=id).update(name=name, department=department)
        else:
            messages.info(request, "You don’t have permission to update employee.")
    return redirect('/employee/')

def delete_employee(request, id):
    permissioned = user_permission(request, 'delete_employee')
    if permissioned:
        employee = Employee.objects.get(id=id)
        return render(request, 'user/pages/modules/employee/delete_employee.html', {'employee': employee})
    else:
        messages.info(request, "You don’t have permission to delete employee.")
    return redirect('/employee/')

def delete_employee_confirmed(request, id):
    permissioned = user_permission(request, 'delete_employee')
    if permissioned:
        employee = Employee.objects.get(id=id)
        employee.delete()
    else:
        messages.info(request, "You don’t have permission to delete employee.")
    return redirect('/employee/')

def export(request):
    permissioned = user_permission(request, 'export_employee')
    if permissioned:
        return render(request, 'user/pages/modules/employee/export.html')
    else:
        messages.info(request, "You don’t have permission to export employee.")
        return redirect('/employee/')


def export_all_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="employee.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name','Department'])

    employees = Employee.objects.all()
    for employee in employees:
        writer.writerow([
            employee.name, 
            employee.department.name
        ])
    return response

def export_all_pdf(request):
    employees = Employee.objects.all()
    open('templates/user/pages/modules/employee/pdf/pdf_temp.html', "w").write(render_to_string('./././pages/modules/employee/pdf/export_pdf.html', {'employees': employees}))

    pdf = html_to_pdf('./././pages/modules/employee/pdf/pdf_temp.html')
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="List of Employees.pdf"'

    return response


def export_process(request):
    from_date = request.POST['date_from']
    to_date = request.POST['date_to']
    try:
        if from_date and to_date:
            export_as = request.POST.get('export_as')
            if export_as == 'csv':
                return file_export_csv(request, from_date, to_date)
            elif export_as == 'xls':
                return file_export_xls(request, from_date, to_date)
            elif export_as == 'pdf':
                return file_export_pdf(request, from_date, to_date)
            elif export_as == 'txt':
                return file_export_txt(request, from_date, to_date)
            else:
                messages.warning(request, "Field 'Export As' is required.")
                return redirect('/employee/export')
        else:
            messages.warning(request, "Fields 'Date From & To' are required.")
            return redirect('/employee/')
    except:
        messages.warning(request, "There was a problem on your request. Hint: use yyyy-mm-dd format.")
        return redirect('/employee/export')


def file_export_csv(request, from_date, to_date):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Export Employees List.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name','Department'])

    employees = Employee.objects.filter(employed_at__range=[from_date, to_date])
    for employee in employees:
        writer.writerow([
            employee.name, 
            employee.department.name
        ])
    return response


def file_export_xls(request, from_date, to_date):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="Export Departments List.xls"'

    work_book = xlwt.Workbook(encoding='utf-8')
    sheet = work_book.add_sheet('Departments')

    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Name','Department']

    for col_num in range(len(columns)):
        sheet.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    employees = Employee.objects.filter(employed_at__range=[from_date, to_date])
    for employee in employees:
        row_num += 1
        for col_num in range(2):
            if col_num % 2 == 0:
                sheet.write(row_num, col_num, employee.name, font_style)
            else:
                sheet.write(row_num, col_num, employee.department.name, font_style)
    work_book.save(response)
    return response


def file_export_pdf(request, from_date, to_date):
    employees = Employee.objects.filter(employed_at__range=[from_date, to_date])
    open('templates/user/pages/modules/employee/pdf/pdf_temp.html', "w").write(render_to_string('./././pages/modules/employee/pdf/export_pdf.html', {'employees': employees}))

    pdf = html_to_pdf('./././pages/modules/employee/pdf/pdf_temp.html')
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="List of Employees.pdf"'
    return response


def file_export_txt(request, from_date, to_date):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="Export Employees List.txt"'

    writer = csv.writer(response)
    writer.writerow(['Employee', '          Department'])

    employees = Employee.objects.filter(employed_at__gte=from_date, employed_at__lte=to_date)
    for employee in employees:
        writer.writerow([
            employee.name,
            '          '+employee.department.name
        ])
    return response


def print(request):
    permissioned = user_permission(request, 'print_employee')
    if permissioned:
        return render(request, 'user/pages/modules/employee/print.html')
    else:
        messages.info(request, "You don’t have permission to print employee.")
        return redirect('/employee/')


def print_all(request):
    employees = Employee.objects.all()
    return render(request, 'user/pages/modules/employee/pdf/print_pdf.html', {'employees': employees})


def print_process(request):
    from_date = request.POST['date_from']
    to_date = request.POST['date_to']
    try:
        if from_date and to_date:
            return file_print_default(request, from_date, to_date)
        else:
            messages.warning(request, "Fields 'Date From & To' are required.")
            return redirect('/employee/')
    except:
        messages.warning(request, "There was a problem on your request. Hint: use yyyy-mm-dd format.")
        return redirect('/employee/export')


def file_print_default(request, from_date, to_date):
    employees = Employee.objects.filter(employed_at__gte=from_date, employed_at__lte=to_date)
    return render(request, 'user/pages/modules/employee/pdf/print_pdf.html', 
        {
            'employees': employees, 
            'from_date': from_date,
            'to_date': to_date
        }
    )
