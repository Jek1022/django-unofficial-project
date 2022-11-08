from django.shortcuts import render
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View
from django.template.loader import render_to_string
from django.urls import reverse
from django.shortcuts import redirect
from .models import Department
from .forms import DeptForm
from .tables import DeptTable
from .file_process import html_to_pdf 
import csv, xlwt


def user_permission(request, action) -> bool:
    permission = Permission.objects.filter(user=request.user, codename=action)
    return permission


def department(request):
    form = DeptForm()
    table = DeptTable(Department.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=5)
    return render(request, 'user/pages/modules/department/department.html', {'form': form, 'table': table,})

def search(request):
    permissioned = user_permission(request, 'search_department')
    if permissioned:
        keyword = request.GET.get('q')
        if keyword:
            try:
                form = DeptForm()
                results = DeptTable(Department.objects.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword)))
                if results:
                    table = results.paginate(page=request.GET.get('page', 1), per_page=5)
                else:
                    table = "not found."
                return render(request, 'user/pages/modules/department/department.html', {'form': form, 'table': table})
            except:
                messages.error(request, "There was a problem on your search.")
        else:
            messages.info(request, "Please enter your search keyword.")
    else:
        messages.info(request, "You don’t have permission to search department.")
    return redirect('/department/')

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

def export(request):
    permissioned = user_permission(request, 'export_department')
    if permissioned:
        return render(request, 'user/pages/modules/department/export.html')
    else:
        messages.info(request, "You don’t have permission to export department.")
        return redirect('/department/')

def export_all_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="department.csv"'

    writer = csv.writer(response)
    writer.writerow(['Department','Description'])

    departments = Department.objects.all().values_list('name','description')
    for department in departments:
        writer.writerow(department)

    return response

def export_all_pdf(request):
    departments = Department.objects.all()
    open('templates/user/pages/modules/department/pdf/pdf_temp.html', "w").write(render_to_string('./././pages/modules/department/pdf/export_pdf.html', {'departments': departments}))

    pdf = html_to_pdf('./././pages/modules/department/pdf/pdf_temp.html')
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="List of Departments.pdf"'

    return response

def print_department_pdf(request):
    departments = Department.objects.all()
    
    return render(request, 'user/pages/modules/department/pdf/print_pdf.html', {'departments': departments})

def export_process(request):

    from_date = request.POST['date_from']
    to_date = request.POST['date_to']
    try:
        if from_date and to_date:
            export_as = request.POST.get('export_as')
            if export_as == 'csv':
                return file_export_csv(request, from_date, to_date)
            elif export_as == 'xls':
                return file_export_xls(request, from_date, to_date)
            elif export_as == 'pdf':
                return file_export_pdf(request, from_date, to_date)
            elif export_as == 'txt':
                return file_export_txt(request, from_date, to_date)
            else:
                messages.warning(request, "Field 'Export As' is required.")
                return redirect('/department/export')
    except:
        messages.warning(request, "There was a problem on your request. Hint: use yyyy-mm-dd format.")
        return redirect('/department/export')
    else:
        messages.warning(request, "Field 'Date From & To' is required.")
        return redirect('/department/')

def file_export_csv(request, from_date, to_date):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Export Departments List.csv"'

    writer = csv.writer(response)
    writer.writerow(['Department','Description'])

    departments = Department.objects.filter(created_at__gte=from_date, created_at__lte=to_date).values_list('name', 'description')
    for department in departments:
        writer.writerow(department)

    return response

def file_export_xls(request, from_date, to_date):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="Export Departments List.xls"'

    work_book = xlwt.Workbook(encoding='utf-8')
    sheet = work_book.add_sheet('Departments')

    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Department','Description']

    for col_num in range(len(columns)):
        sheet.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    departments = Department.objects.filter(created_at__gte=from_date, created_at__lte=to_date).values_list('name', 'description')
    for department in departments:
        row_num += 1
        for col_num in range(len(department)):
            sheet.write(row_num, col_num, department[col_num], font_style)

    work_book.save(response)
    return response

def file_export_pdf(request, from_date, to_date):
    departments = Department.objects.filter(created_at__gte=from_date, created_at__lte=to_date)
    open('templates/user/pages/modules/department/pdf/pdf_temp.html', "w").write(render_to_string('./././pages/modules/department/pdf/export_pdf.html', {'departments': departments}))

    pdf = html_to_pdf('./././pages/modules/department/pdf/pdf_temp.html')
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="List of Departments.pdf"'

    return response

def file_export_txt(request, from_date, to_date):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="Export Departments List.txt"'

    writer = csv.writer(response)
    writer.writerow(['Department','Description'])

    departments = Department.objects.filter(created_at__gte=from_date, created_at__lte=to_date).values_list('name', 'description')
    for department in departments:
        writer.writerow(department)

    return response

def print(request):
    permissioned = user_permission(request, 'print_department')
    if permissioned:
        return render(request, 'user/pages/modules/department/print.html')
    else:
        messages.info(request, "You don’t have permission to print department.")
        return redirect('/department/')