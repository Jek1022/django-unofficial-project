from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib import messages
from django.shortcuts import redirect
from .tables import EmployeeTable
from .forms import EmployeeForm
from .models import Employee

def user_permission(request, action) -> bool:
    permission = Permission.objects.filter(user=request.user, codename=action)
    return permission

# index page
def employee(request):
    form = EmployeeForm
    table = EmployeeTable(Employee.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=5)
    return render(request, 'user/pages/modules/employee/employee.html', {'form': form, 'table': table})

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