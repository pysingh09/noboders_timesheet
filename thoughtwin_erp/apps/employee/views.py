import json,csv,io
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.views.generic import View,ListView,TemplateView,UpdateView
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.generic import View,ListView,TemplateView,CreateView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login
from employee.models import Profile, EmployeeAttendance, AllottedLeave,LeaveRequest
from employee.forms import SignUpForm, ProfileForm, AllottedLeavesForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date
from django.db.models import Count
from time import sleep
from django.db.models import Sum
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm




def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request,user)
                return redirect('employee:dashboard')
            else:
                return render(request,'registration/login.html',{ 'form':form})
        else:
            form = AuthenticationForm()
        return render(request,'registration/login.html',{ 'form':form})
    else:
        return redirect('employee:dashboard')
            

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return redirect('employee:dashboard')

class Dashboard(View):
    def get(self, request):
        return render(request, 'dashboard/dashboard.html')

# @login_required(login_url='/accounts/login')
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
            # return redirect("login.html")
    else:
        user_form = SignUpForm()
        profile_form = ProfileForm()
    return render(request, 'registration/signup.html',{'user_form': user_form, 'profile_form': profile_form}) 


class EmployeeProfile(TemplateView):
    template_name = "profile.html"

class EmployeeListView(ListView):
    model = Profile
    template_name = "employee_list.html"

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
            # messages.success(self.request, 'Settings saved successfully')
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


# @login_required(login_url='/accounts/login')
@permission_required('admin.con_add_log_entry')
def file_upload(request):
    template = 'file_upload.html'
    prompt= {
             'order' : 'order of csv should be employee_no, in_time, out_time, date'
    }
    if request.method == 'GET':
        return render(request,template,prompt)

    csv_file = request.FILES["csv_file"]
    if not csv_file.name.endswith('.csv'):
        messages.error(request,'this is not csv file')

    file_data = csv_file.read().decode("utf-8")
    io_string =io.StringIO(file_data)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):

        profile = Profile.objects.get(employee_id=column[0])
        in_time = datetime.strptime(column[1] ,'%I:%M%p')
        out_time = datetime.strptime(column[2] ,'%I:%M%p')

        created= EmployeeAttendance.objects.update_or_create(
            user=profile.user,
            employee_id = column[0],
            in_time = in_time,
            out_time =out_time,
            date = column[3],
        )
    messages.success(request, ' file Successfully Uploaded.')
   
    return render(request,template)


# @login_required(login_url='/accounts/login')
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
    # import pdb; pdb.set_trace()
    date_str1 = request.POST.get("dat")
    emp_id = request.POST.get("emp_id")
    # date_str1 = request.POST.get("id")
    date_dt1 = datetime.strptime(date_str1, '%B %d, %Y')
    employee_attendence_date = EmployeeAttendance.objects.filter(date=date_dt1,employee_id=emp_id)
    
    template_name = "partial/date_time_popup.html"
    return render(request,template_name,{ "employee_attendence":employee_attendence_date }) 

def employee_details(request,id):
    attendances_data = EmployeeAttendance.objects.filter(user_id=id)
    names = set()
    result = []
    for att in attendances_data:
        if not att.date in names:
            names.add(att.date)
            result.append(att)
    return render(request,'home.html', {'attendances_data' : result})

def show_calendar(request,id):
    attendances_data = EmployeeAttendance.objects.filter(user_id=id)
    names = set()
    result = []
    
    for att in attendances_data:
        if not att.date in names:
            names.add(att.date)
            result.append(att)

    return render(request,'fullcalendar.html', {'attendances_data' : result})

     

def show (request):
    attendances_data = EmployeeAttendance.objects.filter(user=request.user)
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
        user = request.user.username
        for date_str in request.POST.getlist('leaveRequestArr[]'):
            date_time_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            LeaveRequest.objects.create(user=request.user,date=date_time_obj)
        return JsonResponse({'status': 'success'})
    else:
        return render(request,'request_leave.html')


class LeaveListView(ListView):
    model = LeaveRequest
    template_name = "leave_list.html"

def red_list(request):
    attendances_data = EmployeeAttendance.objects.filter(user=request.user)
    names = set()
    result = []
    # import pdb; pdb.set_trace()
    for att in attendances_data:
        if not att.date in names:
            names.add(att.date)
            result.append(att)

    return render(request,'red_list.html', {'attendances_data' : result})









