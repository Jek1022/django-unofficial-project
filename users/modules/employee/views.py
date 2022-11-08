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
import csv

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


def export_employee_csv(request):
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

def export_employee_pdf(request):
    employees = Employee.objects.all()
    open('templates/user/pages/modules/employee/pdf/pdf_temp.html', "w").write(render_to_string('./././pages/modules/employee/pdf/export_pdf.html', {'employees': employees}))

    pdf = html_to_pdf('./././pages/modules/employee/pdf/pdf_temp.html')
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="List of Employees.pdf"'

    return response

def print_employee_pdf(request):
    employees = Employee.objects.all()
    
    return render(request, 'user/pages/modules/employee/pdf/print_pdf.html', {'employees': employees})
