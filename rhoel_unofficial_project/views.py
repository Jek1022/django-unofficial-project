from django.shortcuts import render
from .models import Department
from .forms import DeptForm


def department(request):
    if request.method == 'POST':
        form = DeptForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = DeptForm
    return render(request, 'user/pages/modules/department.html', {'form': form})


