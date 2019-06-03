import json,csv,io
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.generic import View,ListView,TemplateView,UpdateView
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.generic import View,ListView,TemplateView #CreateView,,DetailView,DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login
from employee.models import Profile, EmployeeAttendance
from employee.forms import SignUpForm,ProfileForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date
from django.db.models import Count
from time import sleep
from django.db.models import Sum

from django.contrib.auth.forms import AuthenticationForm
# Create your views here.


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

@login_required(login_url='/accounts/login')
def signup(request):
    if request.method == 'POST':    
        user_form = SignUpForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            profile = profile_form.save(commit=False)
            profile.user = new_user
            profile.save()
            return redirect("/employeelist/")
            # return redirect("login.html")
    else:
        user_form = SignUpForm()
        profile_form = ProfileForm()
    return render(request, 'registration/signup.html',{'user_form': user_form, 'profile_form': profile_form}) 


def employee_profile(request):
    template_name = "profile.html"
    return render(request,template_name)


class EmployeeListView(ListView):
    model = Profile
    template_name = "employee_list.html"

class EditProfileView(UpdateView): 
    model = Profile
    form_class = ProfileForm
    template_name = 'update.html'
    success_url = "/employeelist/"


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


@login_required(login_url='/accounts/login')
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
            out_time =out_time, #10 : 00 PM
            date = column[3],
            
        )

    context={}
    return render(request,template,context)


@login_required(login_url='/accounts/login')
def home(request):
    if request.user.is_superuser:
        attendances_data = EmployeeAttendance.objects.all()
        names = set()
        result = []
        for att in attendances_data:
            if not att.date in names:
                names.add(att.date)
                result.append(att)

        return render(request,'home.html', {'attendances_data' : result})
    else:
        attendances_data = EmployeeAttendance.objects.filter(user=request.user)
        names = set()
        result = []
        for att in attendances_data:
            if not att.date in names:
                names.add(att.date)
                result.append(att)

        return render(request,'home.html', {'attendances_data' : result})



def calendar(request):
    template_name = "fullcalendar.html"
    return render(request,template_name) 

def date_time_attendence_view(request):
    date_str1 = request.POST.get("dat")
    # date_str1 = request.POST.get("id")
    date_dt1 = datetime.strptime(date_str1, '%B %d, %Y')
    # import pdb; pdb.set_trace()
    employee_attendence_date = EmployeeAttendance.objects.filter(date=date_dt1)
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
    return render(request,'fullcalendar.html',{'result':result})


 # in_out_time = []
 #    if request.user.is_superuser:
 #        attendances_data = EmployeeAttendance.objects.all()
 #        names = set()
 #        result = []
 #        for att in attendances_data:
 #            if not att.date in names:
 #                names.add(att.date)
 #                result.append(att)

 #        return render(request,'home.html', {'attendances_data' : result})
        
 #    else:
 #        attendances_data = EmployeeAttendance.objects.filter(user=request.user)
 #        names = set()
 #        result = []
 #        for att in attendances_data:
 #            if not att.date in names:
 #                names.add(att.date)
 #                result.append(att)

 #    return render(request,'home.html', {'attendances_data' : result })