from django import forms
from .models import Employee
from users.modules.department.models import Department
from django.views.generic import ListView

class EmployeeForm(forms.ModelForm, ListView):
    class Meta:
        model = Employee
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control block w-full px-3 py-1.5 text-base font-normal mb-2 text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none'}),
        }
        fields = {'name', 'department'}
        labels = {'name': 'Employee Name', 'department': 'Department'}

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(), 
        empty_label='-- Select --',
        widget=forms.Select(
            attrs={
                'class': 'form-control block w-full px-3 py-1.5 text-base font-normal mb-2 text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none'
            }
        )
    )