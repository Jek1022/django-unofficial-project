from django.shortcuts import render
from django.contrib.auth.models import Permission
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from .models import Department
from .forms import DeptForm
from .tables import DeptTable

def user_permission(request, action) -> bool:
    permission = Permission.objects.filter(user=request.user, codename=action)
    return permission


def department(request):
    form = DeptForm()
    table = DeptTable(Department.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=5)
    return render(request, 'user/pages/modules/department/department.html', {'form': form, 'table': table,})

def create_department(request):
    if request.method == 'POST':
        permissioned = user_permission(request, 'add_department')
        if permissioned:
            form = DeptForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                messages.warning(request, form.errors.as_text())
        else:
            messages.info(request, "You don’t have permission to add department.")
    return redirect('/department/')

def view_department(request, id):
    permissioned = user_permission(request, 'view_department')
    if permissioned:
        department = Department.objects.get(id=id)
        return render(request, 'user/pages/modules/department/view_department.html', {'department': department})
    else:
        messages.info(request, "You don’t have permission to view department.")
        return redirect('/department/')

def update_department(request, id):
    permissioned = user_permission(request, 'change_department')
    if not request.GET.get('page'):
        if permissioned:
            name = request.POST['name']
            description = request.POST['description']
            Department.objects.filter(id=id).update(name=name, description=description)
        else:
            messages.info(request, "You don’t have permission to update department.")
    return redirect('/department/')

def delete_department(request, id):
    permissioned = user_permission(request, 'delete_department')
    if permissioned:
        department = Department.objects.get(id=id)
        return render(request, 'user/pages/modules/department/delete_department.html', {'department': department})
    else:
        messages.info(request, "You don’t have permission to delete department.")
        return redirect('/department/')

def delete_department_confirmed(request, id):
    permissioned = user_permission(request, 'delete_department')
    if permissioned:
        department = Department.objects.get(id=id)
        department.delete()
        return HttpResponseRedirect(reverse('department'))
    else:
        messages.info(request, "You don’t have permission to delete department.")
        return redirect('/department/')

