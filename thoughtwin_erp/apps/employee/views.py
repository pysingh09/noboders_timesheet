import json,csv,io
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.views.generic import View,ListView,TemplateView,UpdateView
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.generic import View,ListView,TemplateView,CreateView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login
from employee.models import Profile, EmployeeAttendance, AllottedLeave,EmployeeAttendanceDetail,Leave,LeaveDetails
from employee.forms import SignUpForm, ProfileForm, AllottedLeavesForm,LeaveCreateForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date, timedelta
from django.db.models import Count
from time import sleep
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import login, logout
from django.core.mail import EmailMessage,send_mail
import datetime as only_datetime
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.dateparse import parse_date
from django.urls import reverse, reverse_lazy
# permission
from django.contrib.auth.mixins import PermissionRequiredMixin


# this is for file upload
import xlrd
from django.conf import settings
from django.core.files.storage import FileSystemStorage
fs = FileSystemStorage()


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request,user)
                return redirect('employee:profile')
            else:
                return render(request,'registration/login.html',{ 'form':form})
        else:
            form = AuthenticationForm()
        return render(request,'registration/login.html',{ 'form':form})
    else:
        return redirect('employee:profile')
            

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return redirect('employee:profile')

# class Dashboard(View):
#     def get(self, request):
#         return render(request, 'dashboard/dashboard.html')

def signup(request):
    if request.method == 'POST':    
        user_form = SignUpForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            profile = profile_form.save(commit=False)
            profile.created_by = request.user
            profile.user = new_user
            profile.save()
            return redirect("/employeelist/")        
    else:
        user_form = SignUpForm()
        profile_form = ProfileForm()
    return render(request, 'registration/signup.html',{'user_form': user_form, 'profile_form': profile_form}) 


class EmployeeProfile(TemplateView):
    template_name = "profile.html"

class EmployeeListView(ListView):
    model = Profile
    template_name = "employee_list.html"
    ordering = ['-id']
    # def get_context_data(self, **kwargs):
    #    context = super(EmployeeListView, self).get_context_data(**kwargs)
    #    context['object_list'] = self.model.objects.all().order_by('-id')
    #    return context
class AllEmployeeProfile(TemplateView):
    template_name = "employee_profile.html"
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk = kwargs['pk'])
        return render(request,'employee_profile.html',{'employee' : user})

class ListOfProfile(View):
    template_name = "profile.html"
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk = kwargs['pk'])
        return render(request,'profile.html',{'user' : user})
       
class LeaveCreateView(CreateView):
    model = AllottedLeave
    form_class = AllottedLeavesForm
    template_name = "leave.html"
    success_url = "/leaves/"

    def get_context_data(self, **kwargs):
        return dict( super(LeaveCreateView, self).get_context_data(**kwargs), leave_list=AllottedLeave.objects.all() )

class EditAllotedLeaveView(UpdateView): 
    model = AllottedLeave
    form_class = AllottedLeavesForm
    template_name = 'update_leave.html'
    success_url = "/leaves/"

class EditProfileView(UpdateView): 
    model = Profile
    form_class = ProfileForm
    template_name = 'update.html'
    success_url = "/employeelist/"

    def post(self, request, *args, **kwargs):
        instance = Profile.objects.get(pk = kwargs['pk'])
        form = self.form_class(data=request.POST, instance=instance)
        if form.is_valid():
            userdata = form.save()
            userdata.user.first_name = form.data['first_name']
            userdata.user.last_name = form.data['last_name']
            userdata.user.save()
            return HttpResponseRedirect("/employeelist/")
        else:
            return render(request,'update.html',{'form':form})

@csrf_exempt
def delete_record(request):
    try:    
        for pk in request.POST.getlist('pk[]'):
            obj = EmployeeAttendance.objects.get(pk=pk)
            obj.delete()
        return JsonResponse({'status' :'success'})
    except Exception as e:
        print("Uh Oh!, we met some error:", str(e))
        return JsonResponse({'status' :'false'})

        
@csrf_exempt
def deactivate_user(request,pk):
    profile = Profile.objects.get(pk=pk)
    if request.method == 'POST':
        profile.user.is_active = request.POST.get('is_active')
        profile.user.save()
    return JsonResponse({'status': 'success'})

@permission_required('admin.con_add_log_entry')
def file_upload(request):
    try:
        template = 'file_upload.html'
        prompt= {
                 'order' : 'order of csv should be employee_no, in_time, out_time, date'
        }
        if request.method == 'GET':
            return render(request,template,prompt)
        
        excel_file = request.FILES["excel_file"]
        filename = fs.save(excel_file.name,excel_file)
        file_url = settings.PROJECT_APPS + fs.url(filename) # project app url + filename
        wb = xlrd.open_workbook(file_url)
        sheet = wb.sheet_by_index(0) 
        for i in range(sheet.nrows):
            if i == sheet.nrows-1: # row-1 
                break
            name = sheet.cell_value(i+1,1)
            
            employee_id = sheet.cell_value(i+1,0)
            in_time = sheet.cell_value(i+1,2)    
            out_time = sheet.cell_value(i+1,3)
            dat = sheet.cell_value(i+1,4).split('/')
       

            # in_time = datetime.strptime(in_time ,'%H:%M')
            # out_time = datetime.strptime(out_time ,'%H:%M')
            if in_time =='--:--' and out_time =='--:--':
                in_time = datetime.strptime('00:00' ,'%H:%M')
                out_time = datetime.strptime('00:00' ,'%H:%M')
            elif out_time =='--:--':
                in_time = datetime.strptime(in_time ,'%H:%M')
                out_time = datetime.strptime('23:59' ,'%H:%M')
            else:
                in_time = datetime.strptime(in_time ,'%H:%M')
                out_time = datetime.strptime(out_time ,'%H:%M')

            profile = Profile.objects.get(employee_id=employee_id)   
            
            emp, created = EmployeeAttendance.objects.update_or_create(
                user=profile.user,
                employee_id = employee_id,
                date = dat[2]+'-'+dat[1]+'-'+dat[0],
                created_by=request.user
            )

            if emp:
                detail = EmployeeAttendanceDetail.objects.update_or_create(
                employee_attendance=emp,
                in_time = in_time,
                out_time = out_time,
            )


        messages.success(request, ' File Successfully Uploaded.')
     
       
        return render(request,template)
    except:

        messages.error(request, ' File Upload Failed')
        return render(request,template)

def home(request):
    attendances_data = EmployeeAttendance.objects.filter(user=request.user)
    names = set()
    result = []
    for att in attendances_data:
        if not att.date in names:
            names.add(att.date)
            result.append(att)

    return render(request,'home.html', {'attendances_data' : result})

def date_time_attendence_view(request):
    attendance = EmployeeAttendance.objects.get(id = request.POST.get("attendance_id"))
    template_name = "partial/date_time_popup.html"
    return render(request,template_name,{ "employee_attendence":attendance }) 

def employee_details(request,id):
    attendances_data = EmployeeAttendance.objects.filter(user_id=id)
    return render(request,'home.html', {'attendances_data' : attendances_data})


def show_hour_calender(request):
    attendances_data = EmployeeAttendance.objects.filter(user_id=request.user.id)
    names = set()
    result = []
    for att in attendances_data:
        if not att.date in names:
            names.add(att.date)
            result.append(att)

    return render(request,'fullcalendar.html', {'attendances_data' : result})

def show_calendar(request,id):
    attendances_data = EmployeeAttendance.objects.filter(user_id=id)
    names = set()
    result = []
    for att in attendances_data:
        if not att.date in names:
            names.add(att.date)
            result.append(att)

    return render(request,'fullcalendar.html', {'attendances_data' : result})

@csrf_exempt
def request_leave(request):

    import datetime
    if request.method == 'POST':
        date_list = request.POST.getlist('leaveRequestArr[]')
        attendance_request_list = EmployeeAttendance.objects.filter(date__in=date_list ,user=request.user)
        for attendance in attendance_request_list:
            attendance.empatt_leave_status = 2
            attendance.save()
            frm = 'ankita@thoughtwin.com'
            text_content = request.user.username+ ',Leave request send for less hours'   
            email = EmailMessage("Leave request for less hours",text_content,frm,to=["ankita@thoughtwin.com"])
            
            email.send()   
        return JsonResponse({'status': 'success'})
   

class LeaveListView(ListView):
    model = EmployeeAttendance
    template_name = "leave_list.html"

    def get_context_data(self, **kwargs):
        context = super(LeaveListView, self).get_context_data(**kwargs)
        context['object_list'] = self.model.objects.filter(empatt_leave_status__in=[2,3,4])
       

        return context

def attendence_request_list(request):
    attendances = EmployeeAttendance.objects.filter(user=request.user)
    result = []
    for attendance in attendances:
        if attendance.date_time_diffrence() < timedelta(hours=9):
            result.append(attendance)
        
    return render(request,'red_list.html', {'attendance_data' : result})
    
def leave_status(request): # reject/accept leave hour
    leave_id = request.POST.get("leave_id")
    employee_attendance = EmployeeAttendance.objects.get(id=leave_id)
    employee_attendance. empatt_leave_status = request.POST.get("leave_type")
    employee_attendance.save()
    message = "dummy"
    if employee_attendance. empatt_leave_status == '3':
        message = employee_attendance.user.username +",Leave accept by "+request.user.username+" for less hour"
    if employee_attendance. empatt_leave_status == '4':
        message = employee_attendance.user.username +",Leave reject by "+request.user.username+" for less hour"

    frm = 'ankita@thoughtwin.com'
    email = EmailMessage("Leave response for less hour",message,frm,to=["ankita@thoughtwin.com"])
    email.send()
    
    return JsonResponse({'status': 'success'})

@csrf_exempt
def delete_record(request):
   if request.method == 'POST':
    data = request.POST.getlist('data[]')
    empatt = EmployeeAttendance.objects.filter(id__in=data)
    empatt.delete()
    return JsonResponse({'status': 'success'})

# class RequestLeaveView(PermissionRequiredMixin,CreateView):
class RequestLeaveView(CreateView):
    # permission_required = ('quotes.add_quote', )
    # raise_exception = True
    model = Leave
    form_class = LeaveCreateForm
    template_name = 'request_leave.html'
    success_url = '/leave/'

    def form_valid(self,form):
        try:
            form = self.form_class(data=form.data)
            leave = form.save(commit=False)
            if 'starttime' in form.data:
                starttime = form.data['starttime']
                starttime = datetime.strptime(starttime ,'%H:%M')

                endtime = form.data['endtime']
                endtime = datetime.strptime(endtime ,'%H:%M')
                if starttime >= endtime:
                    messages.error(self.request, 'End Time not valid')
                    return render(self.request,"request_leave.html",{'message':'End Time not valid','form':form})
                

                starttime = starttime.strftime('%I:%M %p')
                endtime = endtime.strftime('%I:%M %p')
                

                leave.starttime = form.data['starttime']
                leave.endtime = form.data['endtime']
            
            startdate = form.data['startdate'].split('-')
            enddate = form.data['enddate'].split('-')
            d1 = date(int(startdate[0]),int(startdate[1]),int(startdate[2]))  # start date
            d2 = date(int(enddate[0]),int(enddate[1]),int(enddate[2]))  # start date
            delta = d2 - d1
            for i in range(delta.days + 1):
                emp, created = EmployeeAttendance.objects.update_or_create(user=self.request.profile.user,employee_id = self.request.profile.employee_id,date = d1 + timedelta(days=i),created_by=self.request.user,empatt_leave_status=5)
            leave.leave_type = form.data['leave_type']
            leave.user = self.request.user
            leave.save()
            leaveDetail = LeaveDetails.objects.create(leave=leave,reason=form.data['reason'],created_by=self.request.user)


            content = render_to_string('email_content.html',{'email_user':self.request.user,'startdate':d1 + timedelta(days=i), 'enddate':d2 + timedelta(days=i),'reason':form.data['reason']})
            text_content = strip_tags(content)
            

            emails = self.request.POST.get('emails').split(',')
            frm = 'ankita@thoughtwin.com'
            user_name =  self.request.user.email
        
            email = EmailMessage("Leave Request",text_content,frm,to=emails)
            email.send()
            
           
            messages.success(self.request, 'Successfully Leave Request Send')
            return HttpResponseRedirect('/leave')
        except:
            # pass 
            messages.error(self.request,'Leave Request Already Send')
            return HttpResponseRedirect('/leave')
                

    def get_context_data(self, **kwargs):
        context = super(RequestLeaveView, self).get_context_data(**kwargs)
        context['object_list'] = self.model.objects.all()
        email_data = []
        for user in User.objects.all():
            email_data.append(user.email)
        context['emails'] = email_data
        return context

class EmpLeaveListView(ListView):
    model = Leave
    template_name = "leave/leave_list.html"
    # def get_context_data(self, **kwargs):
    #     context = super(FullLeaveListView, self).get_context_data(**kwargs)
    #     context['object_list'] = self.model.objects.filter(emp_leave_type__in=[3,4,5])
    #     return context


def full_leave(request):
    try:
        if request.method == 'POST':
            dateleave=[]
            user = request.user
            emp_id = request.user.id
            start = request.POST.get('start_date')
            end = request.POST.get('end_date')
            emp_type = request.POST.get('emp_type')
            start_date = parse_date(start)
            end_date = parse_date(end)
            delta = end_date - start_date
            for i in range(delta.days + 1):
                date = start_date + timedelta(days=i)
                EmployeeAttendance.objects.update_or_create(user = user,employee_id = emp_id,date = date,empatt_leave_status=emp_type)                       
        return JsonResponse({'status': 'success'})
    except Exception as e:
            messages.error(request, 'Already Exist')
            return render(request,'fullday_leave_list.html',)

def full_leave_status(request):
    if request.method == 'POST':
        leave_id =request.POST.get("leave_id")
        leave_user =request.POST.get("leave_user")
        leave_status = request.POST.get("leave_status")
        leave = Leave.objects.get(id=leave_id)
        leave.status = request.POST.get("leave_status")
        leave.save()

        leavedetails = LeaveDetails.objects.filter(leave=leave)
        for leavedetail in leavedetails:
            
            LeaveDetails.objects.create(leave=leave, status = request.POST.get("leave_status") ,reason = leavedetail.reason ,created_by=request.user)    
        startdate = leave.startdate
        enddate = leave.enddate
        delta = enddate - startdate
        for i in range(delta.days + 1):
            employee_attendence = EmployeeAttendance.objects.get(user = leave.user,date = startdate + timedelta(days=i))
            
            if leave_status == '2':    
                employee_attendence.empatt_leave_status = 6
            if leave_status == '3':
                employee_attendence.empatt_leave_status = 7
            employee_attendence.save()

        if leave.status == '2':
            message = leave.user.username +",Leave accept by "+request.user.username
        if leave.status == '3':
            message = leave.user.username +",Leave reject by "+request.user.username

        frm = 'ankita@thoughtwin.com'
        email = EmailMessage("Leave Response",message,frm,to=["ankita@thoughtwin.com"])
        email.send()
    return JsonResponse({'status': 'success'})


class FullLeaveListView(ListView):
    model = EmployeeAttendance
    template_name = "fullday_leave_list.html"
    def get_context_data(self, **kwargs):
        context = super(FullLeaveListView, self).get_context_data(**kwargs)
        context['object_list'] = self.model.objects.filter(empatt_leave_status__in=[2,3,4,5])
        return context