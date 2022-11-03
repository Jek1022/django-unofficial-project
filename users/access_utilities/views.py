from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .tables import AccessUtilityTable
from .forms import AccessUtilityForm

def user_permission(request, action) -> bool:
    permission = Permission.objects.filter(user=request.user, codename=action)
    return permission

def access_utilities(request):
    form = AccessUtilityForm()
    table = AccessUtilityTable(Permission.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=5)
    return render(request, 'user/pages/access_utilities/access_utilities.html', {'form': form, 'table': table})

def create_permission(request):
    if request.method == 'POST':
        permissioned = user_permission(request, 'add_permission')
        if permissioned:
            form = AccessUtilityForm(request.POST)
            if form.is_valid():
                messages.success(request, 'Access under development.')
            else:
                messages.warning(request, form.errors.as_text())
        else:
            messages.info(request, "You don’t have permission to add access utilities.")
    return redirect('/access-utilities/')