"""rhoel_unofficial_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from users.modules.department import views as department_views
from users.modules.employee import views as employee_views
from users.access_utilities import views as access_utilities_views

admin.site.site_header = "PDI Unofficial Project Admin"
admin.site.site_title = "PDI Unofficial Project Admin Portal"
admin.site.index_title = "Welcome to PDI Unofficial Project"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='user/home.html'), name='home'),
    path('__reload__/', include('django_browser_reload.urls')),

    path('access-utilities/', access_utilities_views.access_utilities, name='access_utilities'),
    path('access-utilities/create/', access_utilities_views.create_permission, name='create_permission'),

    path('department/', department_views.department, name='department'),
    path('department/search/', department_views.search, name='search_department'),
    path('department/create/', department_views.create_department, name='add_department'),
    path('department/<int:id>/update/', department_views.update_department, name='update_department'),
    path('department/<int:id>/read/', department_views.view_department, name='view_department'),
    path('department/<int:id>/delete/', department_views.delete_department, name='delete_department'),
    path('department/<int:id>/delete/confirmed', department_views.delete_department_confirmed),
    path('department/export', department_views.export, name='department_export_page'),
    path('department/export/csv', department_views.export_all_csv, name='department_export_all_csv'),
    path('department/export/pdf', department_views.export_all_pdf, name='department_export_all_pdf'),
    path('department/export/process', department_views.export_process, name='department_export_process'),
    path('department/print', department_views.print, name='department_print_page'),
    path('department/print/pdf', department_views.print_all_pdf, name='department_print_all_pdf'),
    path('department/print/process', department_views.print_process, name='department_print_process'),

    path('employee/', employee_views.employee, name='employee'),
    path('employee/search/', employee_views.search, name='search_employee'),
    path('employee/create/', employee_views.create_employee, name='add_employee'),
    path('employee/<int:id>/update/', employee_views.update_employee, name='update_employee'),
    path('employee/<int:id>/read/', employee_views.view_employee, name='view_employee'),
    path('employee/<int:id>/delete/', employee_views.delete_employee, name='delete_employee'),
    path('employee/<int:id>/delete/confirmed', employee_views.delete_employee_confirmed),
    path('employee/export', employee_views.export, name='employee_export_page'),
    path('employee/export/csv', employee_views.export_all_csv, name='employee_export_all_csv'),
    path('employee/export/pdf', employee_views.export_all_pdf, name='employee_export_all_pdf'),
    path('employee/export/process', employee_views.export_process, name='employee_export_process'),
    path('employee/print', employee_views.print, name='employee_print_page'),
    path('employee/print/all', employee_views.print_all, name='employee_print_all'),
    path('employee/print/process', employee_views.print_process, name='employee_print_process'),
]

