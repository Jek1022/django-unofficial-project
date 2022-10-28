from django.shortcuts import render
from django.contrib.auth.models import Permission
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Department
from .forms import DeptForm
from .tables import DeptTable

def user_permission(request, action) -> bool:
    permission = Permission.objects.filter(user=request.user, codename=action)
    return permission


def department(request):
    if request.method == 'POST':
        form = DeptForm(request.POST)
        if form.is_valid() and user_permission(request, 'add_department'):
            form.save()
        else:
            messages.add_message(request, messages.INFO, "You don't have add department access. Please ask assistance to admin.")

    form = DeptForm()
    table = DeptTable(Department.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=5)
    return render(request, 'user/pages/modules/department/department.html', {'form': form, 'table': table,})

def view_department(request, id):
    department = Department.objects.get(id=id)
    return render(request, 'user/pages/modules/department/view_department.html', {'department': department})

def update_department(request, id):
    if not request.GET.get('page'):
        name = request.POST['name']
        description = request.POST['description']

        Department.objects.filter(id=id).update(name=name, description=description)

    form = DeptForm
    table = DeptTable(Department.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=5)
    return render(request, 'user/pages/modules/department/department.html', {'form': form, 'table': table})

def delete_department(request, id):
    department = Department.objects.get(id=id)
    return render(request, 'user/pages/modules/department/delete_department.html', {'department': department})

def delete_department_confirmed(request, id):
    department = Department.objects.get(id=id)
    department.delete()
    return HttpResponseRedirect(reverse('department'))

