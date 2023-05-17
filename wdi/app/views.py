from django.views import View
from django.db.models import Sum
from django.utils import timezone
import json
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import HttpResponse
from .utilities import get_attendance_for_date, get_employees_not_checked_in, get_attendance_for_datetime, get_remaining_project_hours, get_remaining_project_max_hours, format_duration
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import Employee, Project, Ips, Attendance, Resource, Client, ClientContact, Menu, Milestone, Sprint
from datetime import datetime, time, timedelta, date
# from django.contrib.admin.views.decorators import staff_member_required
from .forms import SignUpForm, LoginForm, IpsForm, ProjectForm, EditEmployeeForm, EmployeePasswordChangeForm, CheckoutForm, ReportForm, ResourceForm, AttendanceFilterForm, ClientForm, ClientContactForm, MenuForm, SprintForm
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt


def add_employee(request):
    if request.user.is_authenticated:
        if request.user.hr == True:
            # emp_code = 1001 if Employee.objects.count() == 0 else Employee.objects.aggregate(max=Max('emp_id'))['max']+1
            print("HR >>> True...")
            form = SignUpForm()
            if request.method == "POST":
                
                form = SignUpForm(request.POST,request.FILES)
                if form.is_valid():
                    new_contact = form.save(commit=False)
                    print("not committed...")
                    # new_contact.emp_id = 1001 if Employee.objects.count() == 0 else new_contact.id+1001
                    print("emp id...>>>",new_contact.emp_id)
                    new_contact.save()
                    new_contact.emp_id = 1001 if Employee.objects.count() == 0 else new_contact.id+1000
                    new_contact.save()
                    messages.success(request, 'Employee Created Successfully.')
                    print("Form saved...")
                    return HttpResponseRedirect('/view-employee/')
            return render(request, "app/add_employee.html", {'form':form,'active':'btn-primary'})
        messages.warning(request, 'Only HR...')
        return HttpResponseRedirect('/employee-profile/')        
    return HttpResponseRedirect('/login/')


def view_employee(request):
    if request.user.is_authenticated:
        if request.user.hr == True:
            print("matched...")
            employee_list = Employee.objects.all()
            return render(request,'app/employee_list.html',{'employee_list':employee_list,'active':'btn-primary'})
        else:
            messages.warning(request, 'Only HR...')
            return HttpResponseRedirect('/employee-profile/')
    else:
        return HttpResponseRedirect('/login/')


def edit_employee(request, pk):
    if request.user.is_authenticated:
        if request.user.hr == True:
            emp = Employee.objects.get(pk=pk)
            form = EditEmployeeForm(instance=emp)
            if request.method == "POST":
                form = EditEmployeeForm(request.POST,request.FILES,instance=emp)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/view-employee/')  
        else:
            messages.warning(request, 'Only HR...')
            return HttpResponseRedirect('/employee-profile/')
    else:
        return HttpResponseRedirect('/login/')            
                
    return render(request, "app/edit_employee.html", {'form':form, 'emp':emp,})


def delete_employee(request, pk):
    if request.user.is_authenticated:
        if request.user.hr == True:
            if request.method == 'POST':
                pi = Employee.objects.get(pk=pk)
                pi.delete()
                return HttpResponseRedirect('/view-employee/')
        else:
            messages.warning(request, 'Only HR...')
            return HttpResponseRedirect('/employee-profile/')
    else:
        return HttpResponseRedirect('/login/')


# def delete_employee_profile(request, pk):
#     if request.user.is_authenticated:
#         if request.user.hr == True:
#             if request.method == 'POST':
#                 pi = EmployeeProfile.objects.get(pk=pk)
#                 pi.delete()
#                 return HttpResponseRedirect('/view-employee-profile/')
#         else:
#             messages.warning(request, 'Only HR...')
#             return HttpResponseRedirect('/employee-profile/')
#     else:
#         return HttpResponseRedirect('/login/')


def delete_ips(request, pk):
    if request.user.is_authenticated:
        if request.user.acc == True:
            if request.method == 'POST':
                pi = Ips.objects.get(pk=pk)
                pi.delete()
                return HttpResponseRedirect('/view-ips/')
        else:
            messages.warning(request, 'Only ACCOUNTS...')
            return HttpResponseRedirect('/employee-profile/')
    else:
        return HttpResponseRedirect('/login/')


def delete_resource(request, pk):
    if request.user.is_authenticated:
        if request.user.acc == True:
            if request.method == 'POST':
                pi = Resource.objects.get(pk=pk)
                pi.delete()
                return HttpResponseRedirect('/view-resource/')
        else:
            messages.warning(request, 'Only ACCOUNTS...')
            return HttpResponseRedirect('/employee-profile/')
    else:
        return HttpResponseRedirect('/login/')


# def delete_task(request, pk):
#     if request.user.is_authenticated:
#         if request.user.acc == True:
#             if request.method == 'POST':
#                 pi = Task.objects.get(pk=pk)
#                 pi.delete()
#                 return HttpResponseRedirect('/view-task/')
#         else:
#             messages.warning(request, 'Only ACCOUNTS...')
#             return HttpResponseRedirect('/employee-profile/')
#     else:
#         return HttpResponseRedirect('/login/')


def delete_project(request, pk):
    if request.user.is_authenticated:
        if request.user.acc == True:
            if request.method == 'POST':
                pi = Project.objects.get(pk=pk)
                pi.delete()
                return HttpResponseRedirect('/view-project/')
        else:
            messages.warning(request, 'Only ACCOUNTS...')
            return HttpResponseRedirect('/employee-profile/')
    else:
        return HttpResponseRedirect('/login/')


def delete_client(request, pk):
    if request.user.is_authenticated:
        if request.user.acc == True:
            if request.method == 'POST':
                pi = Client.objects.get(pk=pk)
                pi.delete()
                return HttpResponseRedirect('/view-client/')
        else:
            messages.warning(request, 'Only ACCOUNTS...')
            return HttpResponseRedirect('/employee-profile/')
    else:
        return HttpResponseRedirect('/login/')


def delete_client_contact(request, pk):
    if request.user.is_authenticated and (request.user.acc or request.user.hr):
        if request.method == 'POST':
            pi = ClientContact.objects.get(pk=pk)
            pi.delete()
            return HttpResponseRedirect('/view-client-contact/')
    else:
        return HttpResponseRedirect('/login/')


def employee_login(request):
    print("login entered....")
    if not request.user.is_authenticated:
        print("not authenticated.....")
        if request.method == 'POST':
            print("inside post request.....")
            form = LoginForm(data=request.POST)
            print("form....")
            # form = LoginForm(request=request,data=request.POST)
            if form.is_valid():
                email=form.cleaned_data['email']
                print(email)
                epass=form.cleaned_data['password']
                print(epass)
                user = authenticate(email=email,password=epass)
                print(user)
                if user:
                    login(request, user)
                    current_datetime = timezone.now()
                    print(current_datetime,timezone.now())
                    print("date: ",current_datetime.date())
                    emp_status = Attendance.objects.filter(employee=user, date=current_datetime.date(), status=('AB')).first()
                    print("Attendance Status: ",emp_status)
                    if not emp_status:
                        print("Attendance Mark Nahi Hai...")
                        checkin_exists = Attendance.objects.filter(employee=user, date=current_datetime.date(), checkin__isnull=False).exists()
                        print("check-in-exist: ",checkin_exists)
                        if not checkin_exists:
                            print("Checkin not exist..")
                            attendance = Attendance(employee=user, checkin=timezone.now(), date=current_datetime.date(), status=('PR'))
                            print("Check-In:...",attendance.checkin)
                            attendance.save()
                            print("Check-In saved...")
                            messages.success(request,'Checked-IN Successfully for today!!')
                            return redirect('/employee-dashboard/')
                    print("Login after attendance....")
                    print("Absent Mark Hai..")
                    messages.success(request,'Log-IN Successfully!!')
                    return redirect('/employee-dashboard/')
                messages.success(request,'Wrong Credentials!!')
                return redirect('/login/')        
                        
        else:            
            form = LoginForm()
        
    else:
        return HttpResponseRedirect('/employee-profile/')
    return render(request, 'app/login.html', {'form':form})


def employee_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


# def task_hours_view(request):
#     projects = Project.objects.filter(status="IP")
#     employees = Employee.objects.all()
#     employee_tasks = {}
#     for employee in employees:        
#         employee_tasks[employee.name] = []
#         # print("employee_tasks : ",employee_tasks)
#         for project in projects:
#             # print("Projects: ",project)
#             tasks = Task.objects.filter(project=project)
#             # print("Tasks: ",tasks)
#             for task in tasks:
#                 resource = Resource.objects.filter(task=task, employee=employee).first()
#                 if resource:
#                     assigned_hours = resource.hours
#                     print("type: ", type(assigned_hours))
#                     ips = Ips.objects.filter(task=task, employee=employee).aggregate(total=Sum('hours'))
#                     consumed_hours = ips['total'] if ips['total'] else timedelta(hours=0,minutes=0)
#                     print("type: ", type(consumed_hours))
#                     print("Break...")
#                     print("Consumed Hours: ", consumed_hours)
#                     assigned_hour = int(assigned_hours.total_seconds() / 3600)
#                     consumed_hour = int(consumed_hours.total_seconds() / 3600)
#                     employee_tasks[employee.name].append({
#                         'project': project.project_name,
#                         'task': task.name,
#                         'assigned_hours': assigned_hour,
#                         'consumed_hours': consumed_hour,
#                     })

#     context = {
#         'employee_tasks': employee_tasks
#     }
#     return render(request, 'app/task_hours.html', context)


# def add_ips(request):
#     if request.user.is_authenticated:
#         print("Authenticated")
#         employee = Employee.objects.get(email=request.user)
#         form = IpsForm(employee)
#         if request.method == 'POST':
#             form = IpsForm(employee, request.POST)
#             print("Form...")
#             if form.is_valid():
#                 print("forms validated")
#                 bf = form.save(commit=False)
#                 print("not committed...")
#                 bf.employee = request.user
#                 print("applied request.user...")
#                 print("Hours: ",bf.hours)
#                 print("Hours Type: ",type(bf.hours))
#                 bf.save()
#                 print("saved...")
#                 messages.success(request, 'Ips submitted Successfully.')
#                 return HttpResponseRedirect('/view-ips/')
#     else:
#         return HttpResponseRedirect('/login/')
#     return render(request, "app/add_ips.html", {'form':form})

def add_ips(request):
    if request.user.is_authenticated:
        form = IpsForm()
        print("Before Request.POST..")
        if request.method == 'POST':
            form = IpsForm(request.POST)
            print("Request.POST..",request.POST)
            if form.is_valid():
                print("Form Validated..")
                ips = form.save(commit=False)
                # pro = form.cleaned_data.get('project')
                # print("Pro",pro)
                # project = Project.objects.get(project_name=pro)
                # print("project:",project)
                hour = form.cleaned_data.get('hours')
                hours=int(hour)
                print("Hours: ",hours)
                minute = form.cleaned_data.get('minutes')
                minutes=int(minute)
                print("Minutes...",minutes)
                duration = timedelta(hours=hours, minutes=minutes)
                print("Duration: ",duration)
                ips.hours = duration
                print("Type of IPS Hours: ",type(ips.hours))
                ips.employee = request.user
                # ips.project = project
                ips.save()
                print("Form Saved..")
                messages.success(request, 'Ips submitted Successfully.')
                return HttpResponseRedirect('/view-ips/')
    else:
        return HttpResponseRedirect('/login/')
    return render(request, "app/add_ips.html", {'form': form})


def add_resource(request):
    if request.user.is_authenticated and (request.user.acc or request.user.hr):
        form = ResourceForm()
        print("Authenticated & ADMIN..")
        if request.method == 'POST':
            form = ResourceForm(request.POST)
            if form.is_valid():
                print("forms validated")
                res = form.save(commit=False)
                project = form.cleaned_data.get('project')
                employee = form.cleaned_data.get('employee')
                old=Resource.objects.filter(employee=employee, project=project).exists()
                if old:
                    messages.warning(request, 'Resource already allocated...')
                    # return HttpResponseRedirect('/add-resource/')
                else:
                    hour = int(form.cleaned_data.get('hours'))
                    max_hour = int(form.cleaned_data.get('max_hours'))
                    print('hour: ',hour)
                    print('max_hour: ',max_hour)
                    dur_hour = timedelta(hours=hour)
                    res.hours = dur_hour
                    dur_max_hour = timedelta(hours=max_hour)
                    res.max_hours = dur_max_hour
                    print('duration: ',dur_hour)
                    print('duration: ',dur_max_hour)
                    res.save()
                    print("saved...")
                    messages.success(request, 'Resource allocated Successfully.')
                    return HttpResponseRedirect('/view-resource/')
            print("NOT VALIDTAED....")
        return render(request, "app/add_resource.html", {'form':form})
    else:
        return HttpResponseRedirect('/login/')
    
    
# def add_task(request):
#     if request.user.is_authenticated:
#         print("Authenticated")
#         form = TaskForm(request.POST or None)
#         print("Form...")
#         context = {
#             'form':form
#                 }
#         if form.is_valid():
#             print("forms validated")
#             form.save()
#             print("saved...")
#             messages.success(request, 'Task created successfully.')
#             return HttpResponseRedirect('/view-task/')
#     else:
#         return HttpResponseRedirect('/login/')
#     return render(request, "app/add_task.html", context)


def view_ips(request):
    if request.user.is_authenticated:
        ips_list = Ips.objects.filter(employee=request.user)
        return render(request,'app/view_ips.html',{'ips_list':ips_list})
    else:
        return HttpResponseRedirect('/login/')


def view_resource(request):
    if request.user.is_authenticated and (request.user.acc or request.user.hr):
        resource_list = Resource.objects.all()
        return render(request,'app/resource_list.html',{'resource_list':resource_list})
    else:
        return HttpResponseRedirect('/login/')


def view_ips_all(request):
    if request.user.is_authenticated:
        if request.user.hr and request.user.acc == True:
            ips_list = Ips.objects.all()
            return render(request,'app/ips_list.html',{'ips_list':ips_list})
        else:
            messages.warning(request, 'Only HR...')
            return HttpResponseRedirect('/view-ips/')
    else:
        return HttpResponseRedirect('/login/')


# def edit_ips(request, pk):
#     if request.user.is_authenticated and (request.user.acc or request.user.hr):
#         ips = Ips.objects.get(pk=pk)
#         form = IpsForm(request.POST or None, instance=ips)
#         if request.method == "POST":
#             if form.is_valid():

#                 form.save()
#                 return HttpResponseRedirect('/view-ips/')
#     else:
#         return HttpResponseRedirect('/login/')
                
#     return render(request, "app/edit_ips.html", {'form':form, 'ips':ips,})

# def edit_ips(request, pk):
#     if request.user.is_authenticated and (request.user.acc or request.user.hr):
#         ips = Ips.objects.get(pk=pk)
#         employee = Employee.objects.get(email=request.user)
#         form = IpsForm(employee, request.POST or None, instance=ips)
#         if request.method == "POST":
#             if form.is_valid():
#                 form.save()
#                 return HttpResponseRedirect('/view-ips/')
#     else:
#         return HttpResponseRedirect('/login/')
#     return render(request, "app/edit_ips.html", {'form':form, 'ips':ips})

def edit_ips(request, pk):
    if request.user.is_authenticated and (request.user.acc or request.user.hr):
        ips = get_object_or_404(Ips, id=pk)
        id = ips.id
        abc = str(ips.hours)
        efg = abc.split(':')
        hs = efg[0]
        mns = efg[1]
        print("hours: ",hs)
        print("minutes: ",mns)
        form = IpsForm(instance=ips)
        if request.method == 'POST':
            form = IpsForm(request.POST, instance=ips)
            if form.is_valid():
                ips = form.save(commit=False)
                hour = form.cleaned_data.get('hours')
                hours=int(hour)
                print("Hours: ",hours)
                minute = form.cleaned_data.get('minutes')
                minutes=int(minute)
                print("Minutes...",minutes)
                duration = timedelta(hours=hours, minutes=minutes)
                print("Duration: ",duration)
                ips.hours = duration
                ips.save()
                messages.success(request, 'Ips updated Successfully.')
                return HttpResponseRedirect('/view-ips-all/')
        return render(request, "app/edit_ips.html", {'form': form,'id':id,'hs':hs,'mns':mns})
    else:
        return HttpResponseRedirect('/login/')


def edit_resource(request, pk):
    if request.user.is_authenticated and (request.user.acc or request.user.hr):
        resource = Resource.objects.get(pk=pk)
        hr = resource.hours
        mx_hr = resource.max_hours
        if hr:
            h = int(resource.hours.total_seconds()/3600)
        else:
            h = 'No Record'
        if mx_hr:
            m_h = int(resource.max_hours.total_seconds()/3600)
        else:
            m_h = 'No Record'
        form = ResourceForm(request.POST or None, instance=resource)
        if request.method == "POST":
            print("POST: ",request.POST)
            if form.is_valid():
                res = form.save(commit=False)
                hour = int(form.cleaned_data.get('hours'))
                max_hour = int(form.cleaned_data.get('max_hours'))
                print('hour: ',hour)
                print('max_hour: ',max_hour)
                dur_hour = timedelta(hours=hour)
                res.hours = dur_hour
                dur_max_hour = timedelta(hours=max_hour)
                res.max_hours = dur_max_hour
                print('duration: ',dur_hour)
                print('duration: ',dur_max_hour)
                res.save()
                print("saved...")
                messages.success(request, 'Resource allocated Successfully.')
                return HttpResponseRedirect('/view-resource/')
        return render(request, "app/edit_resource.html", {'form':form, 'resource':resource,'h':h,'m_h':m_h})
    else:
        return HttpResponseRedirect('/login/')            
                
    


# def edit_task(request, pk):
#     if request.user.is_authenticated:
#         if request.user.acc == True:
#             task = Task.objects.get(pk=pk)
#             form = TaskForm(request.POST or None, instance=task)
#             if request.method == "POST":
#                 if form.is_valid():
#                     form.save()
#                     return HttpResponseRedirect('/view-task/')
#         else:
#             messages.warning(request, 'Only HR...')
#             return HttpResponseRedirect('/view-task/')


#     else:
#         return HttpResponseRedirect('/login/')            
                
#     return render(request, "app/edit_task.html", {'form':form, 'task':task,})


def add_project(request):
    if request.user.is_authenticated:
        if request.user.acc == True:
            print("matched....")
            form = ProjectForm()
            print("Project Form...")
            if request.method == "POST":
                form = ProjectForm(request.POST)
                if form.is_valid():
                    print("form validated")
                    bf = form.save(commit=False)
                    hour = form.cleaned_data.get('hours')
                    max_hour = form.cleaned_data.get('max_hours')
                    print('hour: ',int(hour.total_seconds()))
                    print('max_hour: ',int(max_hour.total_seconds()))
                    hours = int(hour.total_seconds())
                    max_hours = int(max_hour.total_seconds())
                    print('hours: ',hour)
                    print('max_hours: ',max_hour)
                    dur_hour = timedelta(hours=hours)
                    bf.hours = dur_hour
                    dur_max_hour = timedelta(hours=max_hours)
                    bf.max_hours = dur_max_hour
                    print('duration: ',dur_hour)
                    print('duration: ',dur_max_hour)
                    bf.save()
                    print("saved...")
                    messages.success(request, 'Project Added Successfully.')
                    return HttpResponseRedirect('/view-project/')
        else:
            messages.warning(request, 'Only Accounts Staff..')
            return HttpResponseRedirect('/employee-profile/')
    else:
        return HttpResponseRedirect('/login/')
    return render(request, "app/add_project.html", {'form':form})


def add_client_contact(request):
    if request.user.is_authenticated and (request.user.acc or request.user.hr):
        form = ClientContactForm()
        print("client contact Form...")
        if request.method == "POST":
            form = ClientContactForm(request.POST)
            if form.is_valid():
                print("form validated")
                abc = form.save(commit=False)
                print("ABC: ",abc)
                client_id = abc.client
                print("Client ID: ",client_id)
                abc.save()
                print("saved...")
                messages.success(request, 'Contact Added Successfully.')
                return HttpResponseRedirect(f'/cli-con/{client_id.pk}/')
    else:
        return HttpResponseRedirect('/login/')
    return render(request, "app/add_client_contact.html", {'form':form})


def add_client(request):
    if request.user.is_authenticated:
        if request.user.acc == True:
            print("matched....")
            form = ClientForm()
            print("Project Form...")
            if request.method == "POST":
                form = ClientForm(request.POST)
                print("Request POST: ", request.POST)
                if form.is_valid():
                    print("form validated")
                    bf = form.save()
                    print("saved...")
                    messages.success(request, 'Client Added Successfully.')
                    return HttpResponseRedirect('/view-client/')
        else:
            messages.warning(request, 'Only Accounts Staff..')
            return HttpResponseRedirect('/employee-profile/')
    else:
        return HttpResponseRedirect('/login/')
    return render(request, "app/add_client.html", {'form':form})


def view_project(request):
    if request.user.is_authenticated and (request.user.acc or request.user.hr):
        pro_list = Project.objects.all()
        for pro in pro_list:
            a = get_remaining_project_hours(pro.id)
            b = get_remaining_project_max_hours(pro.id)
            print("get_remaining_project_hours: ", a)
            print("get_remaining_project_max_hours: ", b)
            pro.remaining_hours = get_remaining_project_hours(pro.id)
            pro.remaining_max_hours = get_remaining_project_max_hours(pro.id)
        return render(request,'app/project_list.html',{'pro_list':pro_list})
    else:
        return HttpResponseRedirect('/login/')


def view_client_contact(request):
    if request.user.is_authenticated and (request.user.acc or request.user.hr):
        contact_list = ClientContact.objects.all()
        return render(request,'app/contact_list.html',{'contact_list':contact_list})
    else:
        return HttpResponseRedirect('/login/')


def view_client(request):
    if request.user.is_authenticated:
        if request.user.acc == True:
            client_list = Client.objects.all()
            return render(request,'app/client_list.html',{'client_list':client_list})
        else:
            messages.warning(request, 'Only ACCOUNTS...')
            return HttpResponseRedirect('/view-client/')
    else:
        return HttpResponseRedirect('/login/')


# def view_task(request):
#     if request.user.is_authenticated:
#         if request.user.acc == True:
#             task_list = Task.objects.all()
#             return render(request,'app/task_list.html',{'task_list':task_list})
#         else:
#             messages.warning(request, 'Only ACCOUNTS...')
#             return HttpResponseRedirect('/view-task/')
#     else:
#         return HttpResponseRedirect('/login/')


def edit_project(request, pk):
    if request.user.is_authenticated and (request.user.acc or request.user.hr):
        pro = Project.objects.get(pk=pk)
        hrs =int(pro.hours.total_seconds()/3600)
        max_hrs = int(pro.max_hours.total_seconds()/3600)
        form = ProjectForm(request.POST or None, instance=pro)
        if request.method == "POST":
            if form.is_valid():
                print("form validated")
                bf = form.save(commit=False)
                hour = form.cleaned_data.get('hours')
                max_hour = form.cleaned_data.get('max_hours')
                print('hour: ',hour)
                print('max_hour: ',max_hour)
                hours = int(hour)
                max_hours = int(max_hour)
                print('hours: ',hours)
                print('max_hours: ',max_hours)
                dur_hour = timedelta(hours=hours)
                bf.hours = dur_hour
                dur_max_hour = timedelta(hours=max_hours)
                bf.max_hours = dur_max_hour
                print('duration: ',dur_hour)
                print('duration: ',dur_max_hour)
                bf.save()
                print("saved...")
                messages.success(request, "Project details updated successfully.")
                return redirect('/view-project/')
        return render(request, "app/edit_project.html", {'form':form, 'pro':pro, 'hours':hrs,'max_hours':max_hrs})
    else:
        return HttpResponseRedirect('/login/')            
                
    


def edit_client(request, pk):
    if request.user.is_authenticated and (request.user.acc or request.user.hr):
        cli = Client.objects.get(pk=pk)
        form = ClientForm(request.POST or None, instance=cli)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/view-client/')
    else:
        return HttpResponseRedirect('/login/')            
                
    return render(request, "app/edit_client.html", {'form':form, 'cli':cli})


def edit_client_contact(request, pk):
    if request.user.is_authenticated and (request.user.acc or request.user.hr):
        con = ClientContact.objects.get(pk=pk)
        form = ClientContactForm(request.POST or None, instance=con)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/view-client-contact/')
    else:
        return HttpResponseRedirect('/login/')            
                
    return render(request, "app/edit_client_contact.html", {'form':form, 'con':con})


def employee_profile(request):
    if request.user.is_authenticated:
        emp = Employee.objects.get(email=request.user)
        return render(request, 'app/profile.html', {'emp': emp})
    return HttpResponseRedirect('/login/')


def attendance_record(request):
    if request.user.is_authenticated and (request.user.acc or request.user.hr):
        attendance_list = Attendance.objects.all()
        return render(request,'app/attendance_record.html',{'attendance_list':attendance_list})
    else:
        return HttpResponseRedirect('/login/')


def my_attendance_record(request):
    if request.user.is_authenticated:
        emp = request.user
        attendance_list = Attendance.objects.filter(employee=emp)
        return render(request,'app/my_attendance_record.html',{'attendance_list':attendance_list})
    return HttpResponseRedirect('/login/')
    

def employee_details(request, pk):
    if request.user.is_authenticated:
        if request.user.acc or request.user.hr  == True:
            emp = Employee.objects.get(pk=pk)
            return render(request, 'app/details.html', {'emp': emp})
        messages.success(request, 'Only Admin')
    return HttpResponseRedirect('/login/')    
            

def employee_dashboard(request):
    if request.user.is_authenticated and (request.user.acc or request.user.hr):
        checkout_form = CheckoutForm()
        employee = get_object_or_404(Employee, email=request.user)
        current_datetime = timezone.now()
        aaj = current_datetime.date()
        employees_not_checked_in = get_employees_not_checked_in(aaj)
        not_checkin = []
        absent_list = Attendance.objects.filter(date=aaj, status='AB')
        employee_times = get_attendance_for_date(aaj)
        before_1230_employees, after_1230_employees = get_attendance_for_datetime(aaj)
        print("employees_not_checked_in: ",employees_not_checked_in)
        # print("EMP TIMES: ",employee_times)
        print("before_1230_employees: ",before_1230_employees)
        print("after_1230_employees: ",after_1230_employees)
        yesterday = aaj - timedelta(days=1)
        yesterday_ips = Ips.objects.filter(date=yesterday)
        print("This is Yesterday: ",yesterday_ips)
        checkin = Attendance.objects.filter(employee=employee, date=aaj, checkin__isnull=False).first()
        print("This is Check-IN Time: ",checkin)
        if checkin:
            supposed = checkin.checkin + timedelta(hours=9,minutes=15)
            print("Supposed checkout for today: ",supposed)
        else:
            supposed = None
        checkout = Attendance.objects.filter(employee=employee, date=aaj, checkout__isnull=False).first()
        print("This is Check-OUT Time: ",checkout)  
    
        if request.method == 'POST':
            post_data = request.POST.copy()
            post_data['checkout'] = timezone.now()
            print("POST CheckOut : ",post_data['checkout'])
            form = CheckoutForm(post_data)

            print("This is Checkout FOrm with post request: ",form)
            print("REQUEST.POST....",request.POST['checkout'])
            print("Type of checkout: ",type(post_data['checkout']))
            
            if form.is_valid() and checkin and not checkout:
                checkout_time = timezone.now()
                checkin.checkout = checkout_time
                print("Type checkout: ",type(checkout_time))
                print("Type checkin: ",type(checkin.checkin))
                aza = checkout_time-checkin.checkin
                print("Difference : ",aza)
                print("Type of difference : ",type(aza))
                checkin.difference = aza
                checkin.save()
                messages.success(request, 'Successfully Checked-OUT for today!')
                return HttpResponseRedirect('/employee-dashboard/')
            messages.success(request, 'Check-OUT already done for today!')
        context = {
            'emp': employee, 
            'checkout_form': checkout_form, 
            'checkin': checkin, 
            'checkout': checkout,
            'supposed':supposed, 
            'employee_times':employee_times, 
            'yesterday_ips':yesterday_ips,
            'employees_not_checked_in':employees_not_checked_in,
            'absent_list':absent_list,
            'not_checkin':not_checkin,
            'before_1230_employees': before_1230_employees,
            'after_1230_employees': after_1230_employees,
        }
        return render(request, 'app/admin_dashboard.html', context)
    
    else:
        
        if request.user.is_authenticated:
            checkout_form = CheckoutForm()
            current_datetime = timezone.now()
            employee = get_object_or_404(Employee, email=request.user)
            resources = Resource.objects.filter(employee=employee,project__status='IP')
            project_info = []
            for resource in resources:
                project = resource.project
                print(project)
                ips = Ips.objects.filter(employee=employee, project=project)
                print("Task from IPS: ",ips)
                # hours_consumed = sum(ip.hours for ip in ips)
                hour = sum(ip.hours.total_seconds() / 3600.0 for ip in ips)
                hours = int(hour)
                minutes = int((hour - hours) * 60)
                hours_consumed = f"{hours} hrs {minutes} mins"
                project_dict = {
                    'project_name': project.project_name,
                    'hours_assigned': resource.display_duration(),
                    'max_hours_assigned': resource.display_duration_max(),
                    'hours_consumed': hours_consumed
                }
                project_info.append(project_dict)
            print("Project Info: ", project_info)

            # Check if the employee has checked in today
            today = current_datetime.date()
            aaj = current_datetime.date()
            print("TODAY....",today)
            print("AAJ....",aaj)
            absent_employee = Attendance.objects.filter(employee=employee, date=aaj, status='AB')
            employee_checkin = Attendance.objects.filter(employee=employee, date=aaj, checkin__isnull=False).first()
            employee_ips = Ips.objects.filter(employee=employee,date=aaj).exists()
            print("This is Employee Checkin Instance: ",employee_checkin)
            print("This is IPS: ",employee_ips)
            if employee_checkin:
                supposed = employee_checkin.checkin + timedelta(hours=9,minutes=15)
                print("Supposed checkout for today: ",supposed)
            else:
                supposed = None
            checkout = Attendance.objects.filter(employee=employee, date=aaj, checkout__isnull=False).first()
            print("This is Check-OUT Time: ",checkout)
            if request.method == 'POST':
                post_data = request.POST.copy()
                post_data['checkout'] = timezone.now()
                print("POST CheckOut : ",post_data['checkout'])
                form = CheckoutForm(post_data)
                print("This is Checkout FOrm with post request: ",form)
                print("REQUEST.POST....",request.POST['checkout'])
                print("Type of checkout: ",type(post_data['checkout']))
                if absent_employee:
                    messages.success(request, 'Logout directly. You are marked as Absent!')
                    return HttpResponseRedirect('/employee-dashboard/')
                if not employee_ips:
                    print("Ips not filled: ",employee_ips)
                    messages.success(request, 'Please fill the IPS for today...')
                    return HttpResponseRedirect('/add-ips/')
                if form.is_valid() and employee_checkin and not checkout == True:
                    checkout_time = timezone.now()
                    employee_checkin.checkout = checkout_time
                    print("Type checkout: ",type(checkout_time))
                    print("Type checkin: ",type(employee_checkin.checkin))
                    aza = checkout_time-employee_checkin.checkin
                    print("Difference : ",aza)
                    print("Type of difference : ",type(aza))
                    employee_checkin.difference = aza
                    employee_checkin.save()
                    messages.success(request, 'Successfully Checked-OUT for today!')
                    return HttpResponseRedirect('/employee-dashboard/')
                messages.success(request, 'Check-out already done')
                return HttpResponseRedirect('/employee-dashboard/')
                
            return render(request, 'app/employee_dashboard.html', {'emp': employee, 'checkout_form': checkout_form, 'checkin': employee_checkin, 'checkout': checkout,'supposed':supposed, 'projects':project_info})
    return HttpResponseRedirect('/login/')



# def add_employee_profile(request,id=None):
#     if request.user.is_authenticated:
#         if request.user.hr == True:
#             print("Authenticated")
#             form = EmployeeProfileForm(request.POST or None)
#             print("Form...")
#             context = {
#                 'form':form
#                 }
#             if form.is_valid():
#                 print("forms validated")
#                 form.save()
#                 print("form saved...")
#                 messages.success(request, 'Profile Created Successfully.')
#                 return HttpResponseRedirect('/view-employee-profile/')
#         else:
#             messages.warning(request, 'Only HR...')
#             return HttpResponseRedirect('/employee-profile/')            
#     else:
#         return HttpResponseRedirect('/login/')
#     return render(request, "app/add_employee_profile.html", context)


# def employee_profile_list(request):
#     if request.user.is_authenticated:
#         if request.user.hr == True:
#             print("matched...")
#             employee_profile_list = EmployeeProfile.objects.all()
#             return render(request,'app/employee_profile_list.html',{'employee_profile_list':employee_profile_list})
#         messages.warning(request, 'Only HR...')
#         return HttpResponseRedirect('/employee-profile/')


# def edit_employee_profile(request, pk):
#     if request.user.is_authenticated:
#         if request.user.hr == True:
#             emp_pro = EmployeeProfile.objects.get(pk=pk)
#             form = EmployeeProfileForm(request.POST or None, instance=emp_pro)
#             if request.method == "POST":
#                 if form.is_valid():

#                     form.save()
#                     return HttpResponseRedirect('/view-employee-profile/')
#         else:
#             messages.warning(request, 'Only HR...')
#             return HttpResponseRedirect('/employee-profile/')
#     else:
#         return HttpResponseRedirect('/login/')            
                
#     return render(request, "app/edit_employee_profile.html", {'form':form, 'emp_pro':emp_pro})


def attendance_form(request):
    if request.user.is_authenticated and (request.user.acc or request.user.hr):
            form = AttendanceFilterForm(request.POST or None)
            attendance_list = Attendance.objects.all()
            if form.is_valid():
                start_date = form.cleaned_data['start_date']
                print("start date: ",start_date)
                end_date = form.cleaned_data['end_date']
                print("end date: ",end_date)
                employee = form.cleaned_data['employee']
                attendance_list = attendance_list.filter(date__range=[start_date, end_date],employee=employee)
                print("Attendance List: ",attendance_list)
            return render(request,'app/attendance_form.html', {'form': form, 'attendance_list': attendance_list})
    else:
        return HttpResponseRedirect('/login/')


def mark_absent(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        employee = Employee.objects.get(id=employee_id)
        print(employee_id)
        aaj = date.today()
        attendance, created = Attendance.objects.get_or_create(employee=employee, date=aaj, status='AB')
        # attendance.status = 'AB'
        attendance.save()
        return redirect('employee-dashboard')
    

def cli_con(request,pk):
    cli = Client.objects.get(pk=pk)
    con = ClientContact.objects.filter(client=cli)
    print("Client: ",cli)
    print("Client Contacts: ",con)
    return render(request, 'app/client_contactpage.html',{'cli':cli,'con':con})


def check_project_hours(request):
    if request.method == 'GET':
        project_id = request.GET.get('project_id')
        print(project_id)
        if project_id:
            remaining_hours = get_remaining_project_hours(id=project_id)
            remaining_max_hours = get_remaining_project_max_hours(id=project_id)
            print(remaining_hours)
            return JsonResponse({'remaining_hours': remaining_hours,'remaining_max_hours':remaining_max_hours})
    return JsonResponse({})


def get_assigned_projects(request):
    assigned_projects = []
    if request.user.is_authenticated:
        employee = Employee.objects.get(email=request.user)
        resources = Resource.objects.filter(employee=employee)
        assigned_projects = [{'id': resource.project.id, 'project_name': resource.project.project_name} for resource in resources]
    print("assigned_projects",assigned_projects)
    return JsonResponse({'assigned_projects': assigned_projects})


def add_menu(request):
    form = MenuForm()
    print("Menu Form..")
    if request.method == 'POST':
        print("Inside POST Request..")
        form = MenuForm(request.POST)
        if form.is_valid():
            staff = request.POST.get('staff')
            staff_desig = request.POST.get('staff_desig')
            if staff == 'Rushabh Parekh':
                img_url = "https://wordpress.betadelivery.com/Ttg/wp-content/uploads/2023/03/PXL_20230316_2031046283.jpg"
            elif staff == 'Ritesh Pandey':
                img_url = "https://itws.ae/smart-fusion/wp-content/uploads/2023/03/sign-img.png"
            print("Staff: ",staff)
            print("Img Url: ",img_url)
            current = timezone.now()
            print("Current: ",current)
            date = str(current.strftime('%d %B, %Y'))
            print("date: ",date)
            client_name = request.POST.get('client_name')
            for_client = request.POST.get('for_client')
            title = request.POST.get('title')
            email = request.POST.get('email')
            print("Email: ",email)
            template = get_template('foodmenu/index.html')
            context = {'client_name': client_name, 'for_client':for_client, 'title': title, 'date':date, 'img_url':img_url, 'staff':staff, 'staff_desig':staff_desig}
            html = template.render(context)

            result = BytesIO()
            # pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)
            pdf = result.getvalue()

            email = EmailMessage(
                'Contract Agreement',
                'Please find attached Agreement:',
                'wdipl06@gmail.com',
                [email],
                reply_to=['wdipl06@gmail.com']
            )
            email.attach('contract.pdf', pdf, 'application/pdf')
            
            # Send the email
            email.send(fail_silently=False)
            
            # Return a response to the user
            messages.success(request, 'Please check your email..')
            return redirect('employee-profile')
    return render(request, 'app/menu.html', {'form':form})


def project_details(request, pk):
    if request.user.is_authenticated and (request.user.acc or request.user.hr):
        pro = Project.objects.get(pk=pk)
        mile = Milestone.objects.filter(project=pro)
        milestone_dict = {milestone: [{'name': sprint.name, 'duration': format_duration(sprint.hours)} for sprint in Sprint.objects.filter(milestone=milestone)] for milestone in Milestone.objects.filter(project=pro)}
        for milestone, sprints in milestone_dict.items():
            milestone.duration = format_duration(milestone.hours)
            milestone.name = milestone.name

        print('milestone_dict: ',milestone_dict)
        res = Resource.objects.filter(project=pro)
        print('res_dict: ',res)
        utilized_list = [] # create an empty list to hold all utilized dictionaries
        for j in res:
            utilized_hours_sum = Ips.objects.filter(employee=j.employee.id,project=pro).aggregate(Sum('hours'))['hours__sum']
            utilized_hours = format_duration(utilized_hours_sum) if utilized_hours_sum else 'No Record'
            utilized = {
                'res_id':j.id,
                'emp_name':j.employee.first_name,
                'hours_assigned': j.display_duration() if j.hours else 'No Record',
                'max_hours_assigned': j.display_duration_max() if j.max_hours else 'No Record',
                'start_date':j.date,
                'utilized_hours': utilized_hours
            }
            utilized_list.append(utilized)
        print('Ips List: ',utilized_list)
        return render(request, 'app/project_info.html', {'el': pro,'res':res,'utilized_list':utilized_list,'mile':mile,'milestone_dict':milestone_dict})
    else:
        return HttpResponseRedirect('/login/')


def add_sprint(request):
    if request.method == 'POST':
        print("Request POST: ", request.POST)
        mile = int(request.POST.get('mile'))
        milestone = get_object_or_404(Milestone,id = mile)
        name = request.POST.get('name')
        hrs = int(request.POST.get('hours'))
        hours = timedelta(hours=hrs)
        sprint = Sprint.objects.create(milestone=milestone, name=name, hours=hours)
        data = {'status': 'success', 'message': f'Sprint "{sprint.name}" created successfully!'}
        return JsonResponse(data)
    else:
        JsonResponse({
            'success': False
        })


# def add_project_milestone(request):
#     if request.user.is_authenticated and (request.user.acc or request.user.hr):
#             form = ProjectForm(request.POST or None)
#             print("Project Form...")
#             milestone_arr = json.loads(request.POST.get('milestoneArr'))
#             print("MileStone: ",milestone_arr)
#             # if request.method == "POST":
                
#                 # form = ProjectForm(request.POST)
#                 # if form.is_valid():
#                 #     print("form validated")
#                 #     bf = form.save(commit=False)
#                 #     hour = form.cleaned_data.get('hours')
#                 #     max_hour = form.cleaned_data.get('max_hours')
#                 #     print('hour: ',int(hour.total_seconds()))
#                 #     print('max_hour: ',int(max_hour.total_seconds()))
#                 #     hours = int(hour.total_seconds())
#                 #     max_hours = int(max_hour.total_seconds())
#                 #     print('hours: ',hour)
#                 #     print('max_hours: ',max_hour)
#                 #     dur_hour = timedelta(hours=hours)
#                 #     bf.hours = dur_hour
#                 #     dur_max_hour = timedelta(hours=max_hours)
#                 #     bf.max_hours = dur_max_hour
#                 #     print('duration: ',dur_hour)
#                 #     print('duration: ',dur_max_hour)
#                 #     bf.save()
#                 #     print("saved...")
#             return JsonResponse({'success': True})
#                     # messages.success(request, 'Project Added Successfully.')
#                     # return HttpResponseRedirect('/view-project/')
#     else:
#         return JsonResponse({'success': False, 'error': 'Invalid request'})        
#     return render(request, "app/add_project_milestone.html", {'form':form})

def add_project_milestone(request):
    if request.user.is_authenticated and (request.user.acc or request.user.hr):
        if request.method == 'POST':
            form = ProjectForm(request.POST)
            print("RequestPOST: ",request.POST)
            milestone_array = request.POST.get('milestoneArr')
            project = request.POST.get('project')
            print("milestone_array: ",milestone_array)
            print("Project: ",project)

            print("Type of milestone_array: ",type(milestone_array))
            print("Type of Project: ",type(project))
           

            if milestone_array and project:
                data_mile = json.loads(milestone_array)
                data_pro = json.loads(project)

                if any(value == '' for value in data_pro.values()):
                    messages.warning(request, 'Please fill all the form fields..')
                    return redirect('add-project-milestone')

                print("Mile Json Data: ",data_mile)
                print("Pro Json Data: ",data_pro)
                int_pro_hours = int(data_pro['hours']) if data_pro['hours'] else None
                
                int_pro_max_hours = int(data_pro['max_hours']) if data_pro['max_hours'] else None
                
                dur_hr=timedelta(hours=int_pro_hours) if int_pro_hours else None
                dur_max_hr=timedelta(hours=int_pro_max_hours) if int_pro_max_hours else None
                print("Type of Mile JSon Data: ",type(data_mile))
                print("Type of Pro JSon Data: ",type(data_pro))
                client = get_object_or_404(Client, pk=data_pro['client'])
                project_obj = Project.objects.create(
                    project_name=data_pro['project_name'],
                    client=client,
                    client_contact=data_pro['client_contact'],
                    start_date=data_pro['start_date'],
                    delivery_date=data_pro['delivery_date'],
                    currency=data_pro['currency'],
                    project_value=data_pro['project_value'],
                    hours_approvedby=data_pro['hours_approvedby'],
                    sales_rep=data_pro['sales_rep'],
                    project_manager=data_pro['project_manager'],
                    status=data_pro['status'],
                    type=data_pro['type'],
                    hours=dur_hr,
                    max_hours=dur_max_hr,
                    no_milestone=data_pro['no_milestone']
                )
                print("Saved  Project...")
                
                milestone_objs = [Milestone(
                    project=project_obj,
                    name=milestone_data['mileName'],
                    hours=timedelta(hours=float(milestone_data['mileHour'])),
                    delivery_date=milestone_data['mileDate']
                    ) for milestone_data in data_mile
                ]
                print('milestone_objs: ',milestone_objs)
                Milestone.objects.bulk_create(milestone_objs)
                print("Saved  MileStoNes...")
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False})
                
        else:
            form = ProjectForm()
            return render(request, "app/add_project_milestone.html", {'form':form})
    return HttpResponseRedirect('/login/')


# def add_sprint(request):
#     if request.user.is_authenticated and (request.user.acc or request.user.hr):
#         form = SprintForm()
#         print("Authenticated & ADMIN..")
#         if request.method == 'POST':
#             form = SprintForm(request.POST)
#             if form.is_valid():
#                 print("forms validated")
#                 form.save()
#                 messages.success(request, 'Sprint Added Successfully.')
#                 return HttpResponseRedirect('/view-project/')
#         return render(request,'app/add_sprint.html',{'form':form})
#     else:
#         return HttpResponseRedirect('/login/')


def view_sprint(request):
    if request.user.is_authenticated and (request.user.acc or request.user.hr):
        spr_list = Sprint.objects.all()
        return render(request,'app/sprint_list.html',{'spr_list':spr_list})
    else:
        return HttpResponseRedirect('/login/')
    

def delete_sprint(request, pk):
    if request.user.is_authenticated and (request.user.acc or request.user.hr):
        if request.method == 'POST':
            pi = Sprint.objects.get(pk=pk)
            pi.delete()
            return HttpResponseRedirect('/view-sprint/')

    else:
        return HttpResponseRedirect('/login/')
    

def edit_sprint(request, pk):
    if request.user.is_authenticated and (request.user.acc or request.user.hr):
        spr = Sprint.objects.get(pk=pk)
        form = SprintForm(request.POST or None, instance=spr)
        if request.method == "POST":
            if form.is_valid():
                print("form validated")


