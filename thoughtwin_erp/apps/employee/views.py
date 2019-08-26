import json,csv,io
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.views.generic import View,ListView,TemplateView,UpdateView,DetailView
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.generic import View,ListView,TemplateView,CreateView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login
from employee.models import Profile, EmployeeAttendance, AllottedLeave,EmployeeAttendanceDetail,Leave,LeaveDetails
from employee.forms import SignUpForm, ProfileForm, AllottedLeavesForm,LeaveCreateForm,UserProfileForm,changePassForm 
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date, timedelta
from django.db.models import Count
from time import sleep
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import login, logout
from django.core.mail import EmailMessage,send_mail, EmailMultiAlternatives
import datetime as only_datetime
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.dateparse import parse_date
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError
# permission
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.template import loader
from django.contrib.auth.models import Group
# import datetime 
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
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

class UserCreateView(PermissionRequiredMixin,CreateView):
    permission_required = ('employee.add_profile', )
    raise_exception = True
    form_class = SignUpForm
    second_form_class = ProfileForm
    template_name = "registration/signup.html"
    success_url = "/employeelist/"

    def get_context_data(self, **kwargs): 
        context = super(UserCreateView, self).get_context_data(**kwargs)
        if 'form2' not in context:
            context['form2'] = self.second_form_class()
        return context

    def form_invalid(self, form,**kwargs): 
        # context['form'] = super().form_invalid(form)
        context = self.get_context_data(**kwargs)
        context['form2'] = self.second_form_class(self.request.POST)
        # context['form'] = self.form_class(self.request.POST)
        # response = super().form_invalid(form)
        return self.render_to_response(context)
        # response = super().form_invalid(self.second_form_class)
        # self.second_form_class
        # return response
        
    def form_valid(self,form):
        try:
            if self.request.method == 'POST':
                profile_form = ProfileForm(data=self.request.POST)
                user_form = SignUpForm(data=self.request.POST)
                if user_form.is_valid() and profile_form.is_valid():

                    new_user = user_form.save(commit=False)
                    profile = profile_form.save(commit=False)
                    new_user.set_password(user_form.cleaned_data['password1'])
                    new_user.save()

                    profile.created_by = self.request.user
                    profile.user = new_user
                    profile.save()
                    
                    group = Group.objects.get(name=profile.get_designation_display()) 
                    group.user_set.add(new_user)
                    return redirect("/employeelist/")    
                else:
                    user_form = SignUpForm()
                    profile_form = ProfileForm()
                    messages.error(self.request,'Feild Fill Correctly')
                    return render(self.request, 'registration/signup.html',{'form': user_form, 'form2': profile_form}) 

                    

            else:
                user_form = SignUpForm()
                profile_form = ProfileForm()
                return render(self.request, 'registration/signup.html',{'form': user_form, 'form2': profile_form}) 

        except Exception as e:
            # messages.error(self.request,'File Upload Failed')
            # form = EmployeeRegistrationForm(self.request.POST)
            user_form = SignUpForm()
            profile_form = ProfileForm()
            return render(self.request, 'registration/signup.html',{'form': user_form, 'form2': profile_form})



class EmployeeProfile(TemplateView):
    template_name = "profile.html"

class EmployeeListView(PermissionRequiredMixin,ListView):
    permission_required = ('employee.can_view_user_profile_list', )
    raise_exception = True
    model = Profile
    template_name = "employee_list.html"
    ordering = ['-id']


class AllEmployeeProfile(PermissionRequiredMixin,DetailView):
    permission_required = ('employee.can_view_user_profile_list', )
    raise_exception = True 
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk = kwargs['pk'])
        return render(request,'employee_profile.html',{'employee' : user})
    
       
class LeaveCreateView(PermissionRequiredMixin,CreateView):
    permission_required = ('employee.add_allottedleave', )
    raise_exception = True
    model = AllottedLeave
    form_class = AllottedLeavesForm
    template_name = "leave.html"
    success_url = "/leaves/"

    def get_context_data(self, **kwargs):
        return dict( super(LeaveCreateView, self).get_context_data(**kwargs), leave_list= AllottedLeave.objects.all().order_by('-created_at'))

    
    


    # def post(self,request):
    #     if request.method=='POST':
    #         total_alloated_leave = request.POST.get('total_leave')
    #         leave_user = request.POST.get('leave')
    #         alloated_leave_user = AllottedLeave.objects.get(user__username=leave_user)
    #         alloated_leave_user.leave = total_alloated_leave
    #         alloated_leave_user.save()



class EditAllotedLeaveView(PermissionRequiredMixin,UpdateView): 
    permission_required = ('employee.change_allottedleave', )
    raise_exception = True
    model = AllottedLeave
    form_class = AllottedLeavesForm
    template_name = 'update_leave.html'
    success_url = "/leaves/"

class EditProfileView(PermissionRequiredMixin,UpdateView):
    permission_required = ('employee.change_profile', )
    raise_exception = True 
    model = Profile
    form_class = ProfileForm
    template_name = 'update.html'
    success_url = "/employeelist/"

    def post(self, request, *args, **kwargs):
        try:
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
        except Exception as e:
            raise

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

@permission_required('employee.add_employeeattendance', raise_exception=True)
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

        for i in range(sheet.nrows-4):
            if i == sheet.nrows-1: # row-1 
                break
            name = sheet.cell_value(i+4,1)
            
            employee_id = sheet.cell_value(i+4,0)
            in_time = sheet.cell_value(i+4,3)    
            out_time = sheet.cell_value(i+4,sheet.ncols-1) #sheet.cell_value(i+4,3)
            dat = sheet.cell_value(0,7).split('/')
       

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

            
            
            profile = Profile.objects.filter(employee_id=employee_id)
            if profile.exists():
                profile = Profile.objects.get(employee_id=employee_id)   
                
                emp, created = EmployeeAttendance.objects.update_or_create(
                    user=profile.user,
                    employee_id = profile.employee_id,
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
    except Exception as e:
        messages.error(request,'File Upload Failed')
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

@permission_required('employee.can_view_employee_attendance_list', raise_exception=True)
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

# @csrf_exempt
# def request_leave(request):

#     import datetime
#     if request.method == 'POST':
#         date_list = request.POST.getlist('leaveRequestArr[]')
#         attendance_request_list = EmployeeAttendance.objects.filter(date__in=date_list ,user=request.user)
#         for attendance in attendance_request_list:
#             attendance.empatt_leave_status = 2
#             attendance.save()
#             frm = 'ankita@thoughtwin.com'
#             text_content = request.user.username+ ',Leave request send for less hours'   
#             email = EmailMessage("Leave request for less hours",text_content,frm,to=["ankita@thoughtwin.com"])
            
#             email.send()   
#         return JsonResponse({'status': 'success'})
 
class LeaveRequestView(View):
    model = EmployeeAttendance

    def post(self,request):
        import datetime
        if request.method == 'POST':
            date_list = request.POST.getlist('leaveRequestArr[]')
            
            attendance_request_list = EmployeeAttendance.objects.filter(date__in=date_list ,user=request.user)
            for attendance in attendance_request_list:
                # emails = request.POST.getlist('emails[]')
                attendance.empatt_leave_status = 2
                attendance.save()
            

            mail_list = []
            default_mail_list = User.objects.filter(groups__name__in=['MD','HR'])
            for usr in default_mail_list:
                mail_list.append(usr.email)
            request_user = request.user.email            
            mail_list.append(request_user)
            mail_list.append(request.user.profile.teamlead.email)
            mail_list = set(mail_list)

            
            request_send_list = []
            
            request_list = User.objects.filter(groups__name__in=['MD','HR'])
            for usr in request_list:
                # emails.append(usr.email)

                request_send_list.append(usr.first_name +" "+ usr.last_name)            
            request_send_list.append( self.request.user.profile.teamlead.first_name+" "+self.request.user.profile.teamlead.last_name)
            request_send_list = set(request_send_list)
            
            # full_name = []
            # full_name.append(self.request.user.first_name)
            # full_name.append(self.request.user.last_name)
            # user = full_name[0] +" "+ full_name[1]
            full_name = self.request.user.first_name+" "+self.request.user.last_name
            user = full_name.title()


            user_date_list = []

            for date_lists in date_list:
                date_email = date_lists.split("-")
                send_email_data = date(int(date_email[0]),int(date_email[1]),int(date_email[2]))
                user_date_list.append(send_email_data.strftime("%b %d, %Y"))
        
            subject_date = attendance.date.strftime("%b %d, %Y")
            content = render_to_string('email/less_leave_mail_content.html',{'email_user':user,'date_list':user_date_list,'request_send_list':request_send_list,'date_time_diffrence': attendance.date_time_diffrence })
        
            email_subject = "Leave Request For Less Hour ||"" "+user+" "'||'" "+ subject_date
            
            text_content = strip_tags(content)
            msg = EmailMultiAlternatives(email_subject, text_content, settings.FROM_EMAIL, mail_list)
            msg.attach_alternative(content, "text/html")
            msg.send()
            
                # text_content = request.user.username+ ',Leave request send for less hours'   
                # email = EmailMessage("Leave request for less hours",text_content,settings.FROM_EMAIL,to=mail_list)
                
                # email.send()   
            return JsonResponse({'status': 'success'})

     

class LeaveListView(PermissionRequiredMixin,ListView):
    permission_required = ('employee.can_view_employee_attendance_list',)
    raise_exception = True 
    model = EmployeeAttendance
    template_name = "leave_list.html"

    def get_context_data(self, **kwargs):
        context = super(LeaveListView, self).get_context_data(**kwargs)
        context['object_list'] = self.model.objects.filter(empatt_leave_status__in=[2,3,4])
        return context


def attendence_request_list(request):
    attendances = EmployeeAttendance.objects.filter(user=request.user,empatt_leave_status__in=[1,2,3,4,])
    result = []
    email_data = []
    for attendance in attendances:
        if attendance.date_time_diffrence() < timedelta(hours=9):
            result.append(attendance)
    mail_list = []
    default_mail_list = User.objects.filter(groups__name__in=['MD','HR'])
    for usr in default_mail_list:
        mail_list.append(usr.email)
    request_user = request.user.email            
    mail_list.append(request_user)
    mail_list.append(request.user.profile.teamlead.email)
    mail_list = set(mail_list)
    # aaccept_email_data = []
    # default_mail_list = User.objects.filter(groups__name__in=['MD','HR'])     
    # for usr in default_mail_list:
    #         aaccept_email_data.append(usr.email)

    # for user in User.objects.all():
    #         email_data.append(user.email)  
    #         email_data.sort() 
    # return render(request,'red_list.html', {'attendance_data' : result,'emails':mail_list,'aaccept_email_data':aaccept_email_data})
    return render(request,'red_list.html', {'attendance_data' : result,'mail_list':mail_list})



    
# def leave_status(request): # reject/accept leave hour
#     email_data = []
#     leave_id = request.POST.get("leave_id")
#     employee_attendance = EmployeeAttendance.objects.get(id=leave_id)
#     employee_attendance. empatt_leave_status = request.POST.get("leave_type")
#     employee_attendance.save()
#     message = "dummy"
#     if employee_attendance. empatt_leave_status == '3':
#         message = employee_attendance.user.username +",Leave accept by "+request.user.username+" for less hour"
#     if employee_attendance. empatt_leave_status == '4':
#         message = employee_attendance.user.username +",Leave reject by "+request.user.username+" for less hour"

#     frm = 'ankita@thoughtwin.com'
#     email = EmailMessage("Leave response for less hour",message,frm,to=["ankita@thoughtwin.com"])
#     email.send()
    
#     return JsonResponse({'status': 'success'})

class LeaveStatusView(View):

    model = EmployeeAttendance

    def post(self,request):
        leave_id = request.POST.get("leave_id")
        employee_attendance = EmployeeAttendance.objects.get(id=leave_id)
    
        empatt_leave_status = request.POST.get("leave_type")
        if empatt_leave_status == '4':
            employee_attendance.leave_day_time = '0.5'
        if empatt_leave_status == '3':
            employee_attendance.leave_day_time = '1.0'
        employee_attendance.empatt_leave_status = request.POST.get("leave_type")
        employee_attendance.save()
        # message = "dummy"

        # if employee_attendance. empatt_leave_status == '3':
        #     message = employee_attendance.user.username +",Leave accept by "+request.user.username+" for less hour"
        # if employee_attendance. empatt_leave_status == '4':
        #     message = employee_attendance.user.username +",Leave reject by "+request.user.username+" for less hour"


        full_name = employee_attendance.user.first_name+" "+employee_attendance.user.last_name
        user = full_name.title()
        approved_full_name = self.request.user.first_name+" "+self.request.user.last_name
        approved_user = approved_full_name.title()
        mail_list = []
        default_mail_list = User.objects.filter(groups__name__in=['MD','HR'])
        for usr in default_mail_list:
            mail_list.append(usr.email)
        request_user = self.request.user.email            
        mail_list.append(request_user)
        mail_list.append(employee_attendance.user.profile.teamlead.email)
        mail_list = set(mail_list)

        email_date = employee_attendance.date.strftime("%b %d, %Y")
        if employee_attendance. empatt_leave_status == '3':

            email_subject = "Leave Approved For Less Hour ||"" "+user+" "'||'" "+email_date
            content = render_to_string('email/approved_less_leave.html',{'approved_user':approved_user,'user':user,'date':email_date,'date_time_diffrence': employee_attendance.date_time_diffrence })

        if employee_attendance. empatt_leave_status == '4':

            email_subject = "Leave Rejected For Less Hour ||"" "+user+" "'||'" "+email_date              
            content = render_to_string('email/reject_less_leave.html',{'approved_user':approved_user,'user':user,'date':email_date,'date_time_diffrence': employee_attendance.date_time_diffrence })
        
        text_content = strip_tags(content)
        msg = EmailMultiAlternatives(email_subject, text_content, settings.FROM_EMAIL, mail_list)
        msg.attach_alternative(content, "text/html")
        msg.send()
        # email = EmailMessage("Leave response for less hour",message,settings.FROM_EMAIL,to=[employee_attendance.user.email])
        # email.send()
        
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

    def form_valid(self,form,**kwargs):
          
        try:
            form = self.form_class(data=form.data)
            leave = form.save(commit=False)
            leave_date = form.data['startdate'].split('-')
            year = int(leave_date[0])
            # alloated_leave = AllottedLeave.objects.get(user = self.request.user)
            # leave_year =  alloated_leave.year
        
            # if year == datetime.datetime.now().year:
            if 'starttime' in form.data:
       
                starttime = form.data['starttime']
                starttime = datetime.strptime(starttime ,'%H:%M')

                # endtime = form.data['endtime']
                # endtime = datetime.strptime(endtime ,'%H:%M')
                endtime = starttime + timedelta(hours=4)
                # if starttime >= endtime:
                #     messages.error(self.request, 'End Time Not Valid')
                #     email_data = []
                #     email = email_data
                #     for user in User.objects.all():
                #         email_data.append(user.email)
                #         email_data.sort()
                #     return render(self.request,'request_leave.html',{'form':form ,'emails':email})

                starttime = starttime.strftime('%I:%M %p')
                endtime = endtime.strftime('%I:%M %p')
                

                leave.starttime = starttime #form.data['starttime']
                leave.endtime = endtime #form.data['starttime']
            
        
            startdate = form.data['startdate'].split('-')
            enddate = form.data['enddate'].split('-')
            d1 = date(int(startdate[0]),int(startdate[1]),int(startdate[2])) #startdate
            d2 = date(int(enddate[0]),int(enddate[1]),int(enddate[2]))  #startdate
            delta = d2 - d1
            leave_type = form.data['leave_type']

            for i in range(delta.days + 1):
                if leave_type == '2':   
                    emp, created = EmployeeAttendance.objects.update_or_create(user=self.request.profile.user,employee_id = self.request.profile.employee_id,date = d1 + timedelta(days=i),created_by=self.request.user,empatt_leave_status=5,leave_day_time = '0.5')
                if leave_type == '3':
                    emp, created = EmployeeAttendance.objects.update_or_create(user=self.request.profile.user,employee_id = self.request.profile.employee_id,date = d1 + timedelta(days=i),created_by=self.request.user,empatt_leave_status=5,leave_day_time = '1.0')
            leave.leave_type = form.data['leave_type']
            leave.user = self.request.user
            leave.save()
            leaveDetail = LeaveDetails.objects.create(leave=leave,reason=form.data['reason'],created_by=self.request.user)

         
            
            # emails = self.request.POST.get('emails').split(',')
            mail_list = []
            default_mail_list = User.objects.filter(groups__name__in=['MD','HR'])
            for usr in default_mail_list:
                # emails.append(usr.email)
                mail_list.append(usr.email)
            request_user = self.request.user.email            
            mail_list.append(request_user)
            mail_list.append(self.request.user.profile.teamlead.email)
            mail_list = set(mail_list)




            request_send_list = []
            
            request_list = User.objects.filter(groups__name__in=['MD','HR'])
            for usr in request_list:
                # emails.append(usr.email)

                request_send_list.append(usr.first_name +" "+ usr.last_name)            
            request_send_list.append( self.request.user.profile.teamlead.first_name+" "+self.request.user.profile.teamlead.last_name)
            request_send_list = set(request_send_list)
           
            full_name = self.request.user.first_name +" "+ self.request.user.last_name
            user = full_name.title()

            if leave_type == '2':
                content = render_to_string('email/email_content.html',{'email_user':user,'startdate':d1 + timedelta(days=i),'reason':form.data['reason'],'request_send_list':request_send_list})
            if leave_type == '3':
                content = render_to_string('email/email_content.html',{'email_user':user,'startdate':d1 + timedelta(days=i), 'enddate':d2 + timedelta(days=i),'reason':form.data['reason'],'request_send_list':request_send_list})
            start_date = d1 + timedelta(days=i)
            end_date = d2 + timedelta(days=i)
            email_startdate = start_date.strftime("%b %d, %Y")
            email_enddate = end_date.strftime("%b %d, %Y")
            text_content = strip_tags(content)
            if form.data['leave_type'] == '2':
                email_subject = "Leave Request ||"" "+user+" "'||'" "+'Half Day'+" ""||"" "+str(email_startdate)
            if form.data['leave_type'] == '3':    
                email_subject = "Leave Request ||"" "+user+" "'||'" "+'Full Day'" "+"||"" "+str(email_startdate)+"-"+str(email_enddate)
            # email = EmailMessage(email_subject,text_content,settings.FROM_EMAIL,to=mail_list)
            # email.send()

            msg = EmailMultiAlternatives(email_subject, text_content, settings.FROM_EMAIL, mail_list)
            msg.attach_alternative(content, "text/html")
            msg.send()
            
            messages.success(self.request, ' Leave Request Sent Successfully')
            # 'mail_list':mail_list - get mail list
            # return render(self.request,'request_leave.html', {'accept_emails' : mail_lists})
            return HttpResponseRedirect('/leave')
            # else:
            #     messages.error(self.request, 'Leave Are Not Alloted In This Year') 
            #     return HttpResponseRedirect('/leave')  
        except IntegrityError:
            messages.error(self.request, 'Leave Request Already Send') 
            return HttpResponseRedirect('/leave')  

        # except Exception as alloated_leave :
    
        #     messages.error(self.request,'Leave Are Not Alloted')
        #     return HttpResponseRedirect('/leave')

    def get_context_data(self, **kwargs):
        context = super(RequestLeaveView, self).get_context_data(**kwargs)
        context['object_list'] = self.model.objects.all()
        # default_mail_list = User.objects.filter(groups__name__in=['MD','HR'])
        # # email_data = []
        # mail_list = [] 
        # # for user in User.objects.all():
        # #     email_data.append(user.email)
        # #     email_data.sort()
        # for usr in default_mail_list:
        #     mail_list.append(usr.email)
        # context['emails'] = email_data
        mail_list = []
        default_mail_list = User.objects.filter(groups__name__in=['MD','HR'])
        for usr in default_mail_list:
            mail_list.append(usr.email)
        request_user = self.request.user.email            
        mail_list.append(request_user)
        mail_list.append(self.request.user.profile.teamlead.email)
        mail_list = set(mail_list)
        context['mail_list'] = mail_list
        return context

# class EmpLeaveListView(PermissionRequiredMixin,ListView):
class EmpLeaveListView(ListView):    
    # permission_required = ('employee.can_view_leave_list',)
    # raise_exception = True
    model = Leave
    template_name = "leave/leave_list.html"
    ordering = ['-created_at']
    def get_context_data(self, **kwargs):
        context = super(EmpLeaveListView, self).get_context_data(**kwargs)
        if self.request.user.groups.exists():
            group_name = self.request.user.groups.first().name
            if group_name == 'HR' or group_name == 'MD':
                return context

        usr = User.objects.filter(email=self.request.user.email)
        profiles = Profile.objects.filter(teamlead=usr[0])
        users =[]
        for profile in profiles:
            users.append(profile.user)
        context['object_list'] = self.model.objects.filter(user__in=users)
        return context


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
        leave_type =request.POST.get("leave_type")
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
        for day in range(delta.days + 1):

            employee_attendence = EmployeeAttendance.objects.filter(user = leave.user,date = startdate + timedelta(days=day))
            names = set()
            result = []
            for att in employee_attendence:
                if not att.date in names:
                    names.add(att.date)
                    result.append(att) 
            for employee_attendence in result:        
                if leave_status == '2':    
                    employee_attendence.empatt_leave_status = 6
                if leave_status == '3':
                    employee_attendence.empatt_leave_status = 7
                employee_attendence.save()
        
        # if leave.status == '2':
        #     message = leave.user.username +",Leave accept by "+request.user.username
        # if leave.status == '3':
        #     message = leave.user.username +",Leave reject by "+request.user.username
    
        
        aaccept_email_data = []        
        aaccept_email_data.append(leave.user.profile.teamlead.email)
        aaccept_email_data.append(leave.user.email)
        default_mail_list = User.objects.filter(groups__name__in=['MD','HR']) 
        
        for usr in default_mail_list:
            aaccept_email_data.append(usr.email)
        data_email = set(aaccept_email_data)

        email_data = []
        for user in User.objects.all():
            email_data.append(user.email)    

        # request_send_list = []
        # request_list = User.objects.filter(groups__name__in=['MD','HR'])
        # for usr in request_list:
        #     request_send_list.append(usr.get_username())            
        # request_send_list.append(request.user.profile.teamlead.username)
        # request_send_list = set(request_send_list)
       
        full_name = leave.user.first_name +" "+ leave.user.last_name
        user = full_name.title()
        approve_fullname = []
        approve_fullname.append(request.user.first_name)
        approve_fullname.append(request.user.last_name)
        approve_user_fullname = approve_fullname[0]+" "+approve_fullname[1]
        startdate = startdate.strftime("%b %d, %Y")
        enddate = enddate.strftime("%b %d, %Y")        
        if leave.status == '2':
            if leave_type == 'Half day':
                email_subject = "Leave Approved " "||"" " +user+  " "'|| Half Day'" "'||' " "+startdate

                content = render_to_string('email/accept_leave_request_mail.html',{'user':user,'accept_user':approve_user_fullname, 'startdate':startdate,'reason':leavedetail.reason,'daytype':leave_type })
            if leave_type == 'Full day':
                email_subject = "Leave Approved " "||"" " +user+  " "'|| Full Day'" "'||' " "+startdate+"-"+enddate
                content = render_to_string('email/accept_leave_request_mail.html',{'user':user,'accept_user':approve_user_fullname, 'startdate':startdate,'enddate':enddate,'reason':leavedetail.reason,'daytype':leave_type })
        if leave.status == '3':
            if leave_type == 'Half day': 
                email_subject = "Leave Rejected " "||"" " +user+  " "'|| Half Day'" "'||' " "+startdate
                content = render_to_string('email/reject_leave_request_mail.html',{'user':user,'accept_user':approve_user_fullname, 'startdate':startdate,'reason':leavedetail.reason,'daytype':leave_type })
            if leave_type == 'Full day':
                email_subject = "Leave Rejected " "||"" " +user+  " "'|| Full Day'" "'||' " "+startdate+"-"+enddate
                content = render_to_string('email/reject_leave_request_mail.html',{'user':user,'accept_user':approve_user_fullname, 'startdate':startdate,'enddate':enddate,'reason':leavedetail.reason,'daytype':leave_type })
    
        text_content = strip_tags(content)
        msg = EmailMultiAlternatives(email_subject, text_content, settings.FROM_EMAIL, data_email)
        msg.attach_alternative(content, "text/html")
        msg.send() 
        
        # accept_email = EmailMessage("Leave Response",message,settings.FROM_EMAIL,to=data_email)
        # accept_email.send()



        if leave.status == '2': 
            if leave_type == 'Half day':
                email_subject = "OOO ||"" "+user+" "'||'" "+leave_type+" "'||'" "+startdate
                content = render_to_string('email/ooo_email_content.html',{'user':user,'startdate':startdate,'reason':leavedetail.reason  })
            if leave_type == 'Full day':
                email_subject = "OOO ||"" "+user+" "'||'" "+leave_type+" "'||'" "+startdate+"-"+enddate
                content = render_to_string('email/ooo_email_content.html',{'user':user,'startdate':startdate,'enddate':enddate,'reason':leavedetail.reason  })

            text_content = strip_tags(content)
            msg = EmailMultiAlternatives(email_subject, text_content, settings.FROM_EMAIL, email_data)
            msg.attach_alternative(content, "text/html")
            msg.send() 
            # email = EmailMessage("Leave ",text_content,settings.FROM_EMAIL,to=email_data)
            # email.send()
        # if leave.status == '3':
        #     email = EmailMessage("Leave",text_content,settings.FROM_EMAIL,to=aaccept_email_data)
        #     email.send()                
    return JsonResponse({'status': 'success'})


class FullLeaveListView(PermissionRequiredMixin,ListView):
    permission_required = ('employee.can_view_employee_attendance_list',)
    raise_exception = True
    model = EmployeeAttendance
    template_name = "fullday_leave_list.html"
    def get_context_data(self, **kwargs):
        context = super(FullLeaveListView, self).get_context_data(**kwargs)
        context['object_list'] = self.model.objects.filter(empatt_leave_status__in=[2,3,4]).order_by('-created_at')
        return context


def change_password(request):
    try:
        if request.user.is_authenticated:

            form = changePassForm(request.POST or None)

            old_password = request.POST.get("old_password")
            new_password = request.POST.get("new_password")
            re_new_password = request.POST.get("re_new__password")

            if request.POST.get("old_password"):

                user = User.objects.get(username= request.user.username)
                if user.check_password('{}'.format(old_password)) == False:
                    form.set_old_password_flag()

            if form.is_valid():

                user.set_password('{}'.format(new_password))
                user.save()
                update_session_auth_hash(request, user)

                return HttpResponseRedirect('/login/')

            else:
                return render(request, 'change_password.html', {"form": form})

        else:
            return HttpResponseRedirect('/login/')

    except Exception as e:
        raise        


class ForgotPassword(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request,'home.html')
        else:
            return render(request,'registration/forgot-password.html')
    
    def post(self,request):
        try:
            if request.method == 'POST':                
                email = request.POST['email']
                try:
                    user = User.objects.get(email=email)
                except Exception as e:
                    messages.error(self.request, 'Email Not Exist')
                    return HttpResponseRedirect('/forgot-password/')
                    
                password = User.objects.make_random_password()
                user.set_password(password)
                user.save()
                body = "Hi there. \n You have requested a new password for your account on Testing.\nYour temporary password is "+password+""
                send_mail = EmailMessage("Forgot password",body,settings.FROM_EMAIL,to=[user.email])
                send_mail.send() 
                messages.success(self.request, 'Check Your Password In Mail') 
                return HttpResponseRedirect('/forgot-password/')
        except Exception as e:
                raise

        

class ShowLeaveListView(ListView):
    model = Leave
    template_name = "leave/fullday_leave.html"   
    def get_context_data(self, **kwargs):
        context = super(ShowLeaveListView, self).get_context_data(**kwargs)
        context['object_list'] = self.model.objects.filter(user=self.request.user,status__in=[1,2,3]).order_by('-created_at')
        return context

def delete_leave(request):

    if request.method == 'POST':
        leave_id =request.POST.get("leave_id")
        leave_status = request.POST.get("leave_status") 
        delete_leave = Leave.objects.filter(id = leave_id,status__in=[1,2,3])
        delete_leave.delete()
        start_date =request.POST.get("start_date")
        end_date =request.POST.get("end_date")
        emp_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        emp_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        delta = emp_end_date - emp_start_date
        for i in range(delta.days + 1):
            delete_employee_leave = EmployeeAttendance.objects.filter(user=request.profile.user,employee_id = request.profile.employee_id,date =emp_start_date + timedelta(days=i),empatt_leave_status__in=[5,6] )
            delete_employee_leave.delete()
    return JsonResponse({'status': 'success'})
        
    








     
