from socket import fromshare
from django import forms
from django.contrib.auth.models import Permission
from django.views.generic import ListView

class AccessUtilityForm(forms.ModelForm, ListView):
    class Meta:
        model = Permission
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control block w-full px-3 py-1.5 text-base font-normal mb-2 text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none'}),
            'codename': forms.TextInput(attrs={'class': 'form-control block w-full px-3 py-1.5 text-base font-normal mb-2 text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none'}),
        }
        fields = ['name', 'codename']
        labels = {'name': 'Permission Name', 'codename': 'Code Name'}