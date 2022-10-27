from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .tables import EmployeeTable
from .forms import EmployeeForm
from rhoel_unofficial_project.models import Employee

def employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
    form = EmployeeForm
    table = EmployeeTable(Employee.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=5)
    return render(request, 'user/pages/modules/employee/employee.html', {'form': form, 'table': table})

def view_employee(request, id):
    employee = Employee.objects.get(id=id)
    return render(request, 'user/pages/modules/employee/view_employee.html', {'employee': employee})

def update_employee(request, id):
    if not request.GET.get('page'):
        name = request.POST['name']
        department = request.POST['department']

        Employee.objects.filter(id=id).update(name=name, department=department)

    form = EmployeeForm
    table = EmployeeTable(Employee.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=5)
    return render(request, 'user/pages/modules/employee/employee.html', {'form': form, 'table': table})

def delete_employee(request, id):
    employee = Employee.objects.get(id=id)
    return render(request, 'user/pages/modules/employee/delete_employee.html', {'employee': employee})

def delete_employee_confirmed(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()
    return HttpResponseRedirect(reverse('user_employee'))