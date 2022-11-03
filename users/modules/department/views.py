from django.shortcuts import render
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.urls import reverse
from django.shortcuts import redirect
from .models import Department
from .forms import DeptForm
from .tables import DeptTable
import csv, io, datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, mm 
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER 
from reportlab.lib import colors
from django_tables2.export.export import TableExport

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

def export_department_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="department.csv"'

    writer = csv.writer(response)
    writer.writerow(['Department','Description'])

    departments = Department.objects.all().values_list('name','description')
    for department in departments:
        writer.writerow(department)

    return response

def export_department_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    d = datetime.datetime.today().strftime('%Y-%m-%d')
    response['Content-Disposition'] = f'inline; filename="department {d}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    #Data to print
    data = {
        "Department": [
            {"title":"Python","views":500},
            {"title":"Javascript","views":500}
        ]
    }
    #Write PDF
    p.setFont("Helvetica", 15, leading=None)
    p.setFillColorRGB(0.29296875,0.453125,0.609375)
    p.drawString(260,800,"Department List")
    p.line(0,780,1000,780)
    p.line(0,780,1000,780)
    xl = 20
    yl = 750
    #Render data
    for k,v in data.items():
        p.setFont("Helvetica", 15, leading=None)
        p.drawString(xl,yl-12,f"{k}")
        for value in v:
            for key,val in value.items():
                p.setFont("Helvetica",10,leading=None)
                p.drawString(xl,yl-20,f"{key} - {val}")
                yl = yl-60
    p.setTitle(f'Report on {d}')
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

def get_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    # attachment -> for download | inline -> for browser view
    response['Content-Disposition'] = 'inline; filename="Department Report File.pdf"'
    width, height = A4

    def coord(x, y, unit=2):
        x, y = x * unit, height - y * unit
        return x, y

    th_no = '''#'''
    th_name = '''Department'''
    th_description = '''Description'''

    buffer = BytesIO()
    p = canvas.Canvas(response)
    
    # p.drawString(20, 800, "Departments list exported at " + datetime.datetime.today().strftime('%Y-%m-%d'))

    departments = Department.objects.all()
    data = []
    data.append([th_no, th_name, th_description])
    try:
        for index, department in enumerate(departments, start=1):
            
            row = []
            num = str(index).encode('utf-8')
            name = str(department.name).encode('utf-8')
            description = str(department.description).encode('utf-8')
            
            row.append(num)
            row.append(name)
            row.append(description)
            
            data.append(row)

            if index % 10 == 0:
                p.drawString(10, 10, num+name+description)
                p.showPage()
           
    except:
        pass
    # table = Table(data, colWidths=[12 * mm, 70 * mm, 110 * mm])

    # table.setStyle(TableStyle([
    #     ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    #     ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    # ]))
    # table.wrapOn(p, width, height)
    # table.drawOn(p, *coord(8, 5, mm))

    p.setTitle('PDF | Department')
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response