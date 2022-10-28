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
from . import views
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='user/home.html'), name='home'),
    path('__reload__/', include('django_browser_reload.urls')),

    path('department/', views.department, name='department'),
    path('department/<int:id>', views.update_department, name='update_department'),
    path('department/<int:id>/read/', views.view_department, name='view_department'),
    path('department/<int:id>/delete/', views.delete_department, name='delete_department'),
    path('department/<int:id>/delete/confirmed', views.delete_department_confirmed),

    path('employee/', user_views.employee, name='user_employee'),
    path('employee/<int:id>', user_views.update_employee, name='update_employee'),
    path('employee/<int:id>/read/', user_views.view_employee, name='view_employee'),
    path('employee/<int:id>/delete/', user_views.delete_employee, name='user_delete_employee'),
    path('employee/<int:id>/delete/confirmed', user_views.delete_employee_confirmed),
]
