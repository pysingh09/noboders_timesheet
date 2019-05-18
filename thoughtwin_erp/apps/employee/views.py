import json,csv,io
from django.shortcuts import render
from django.views.generic import View,ListView,TemplateView #CreateView,,DetailView,DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login
from employee.models import Profile, EmployeeAttendance
from employee.forms import SignUpForm,ProfileForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from datetime import datetime
def delete_profile(request):        
    user = request.user
    user.is_active = False
    user.save()
    logout(request)
    messages.success(request, 'Profile successfully disabled.')
    return redirect('index')

# @login_required
# def home(request):
#     return render(request,'home.html')
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
            return render(request,'registration/signup.html')
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

def deactivate_user():
    if request.method==POST:
        pk = request.POST.get('pk')
        profile = Profile.objects.get(pk=pk)
        profile.block_profile()

    
def edit(request, id):  
    employee = Profile.objects.get(id=id)  
    return render(request,'edit.html', {'employee':employee})

def update(request, id):  
    employee = Profile.objects.get(id=id)  
    form = ProfileForm(request.POST, instance = employee)  
    if form.is_valid():  
        form.save() 
        return redirect("employee_list.html")  
    return render(request, 'edit.html', {'employee': employee})
    

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
        # in_time= datetime.strptime("column[1]", "%H:%M")
        # out_time= datetime.strptime("column[2]", "%H:%M")
        # in_time.strftime("%I:%M %p")
        # out_time.strftime("%I:%M %p")
        user_profile = Profile.objects.get(employee_id=column[0])
        _, created= EmployeeAttendance.objects.update_or_create(
            user=profile.user,
            employee_id = column[0],
            in_time = column[1],
            out_time =column[2],
            date = column[3]
        )
    context={}
    return render(request,template,context)

@login_required(login_url='/accounts/login')
def home(request):
    context = {}
    if request.user.is_active:
        if request.user.is_superuser:
            context['attendance_data'] = EmployeeAttendance.objects.all()
        else:
            usr = User.objects.get(id = request.user.id)
            context['attendance_data'] = EmployeeAttendance.objects.filter(employee_id=usr.profile.employee_id)
        return render(request,'home.html', context)
    else:
        return redirect('/')


# def user_login(request):
#     context={}
#     if request.method == 'POST':
#         username=request.POST['username']
#         password=request.POST['password']
#         user=authenticate(request,username=username,password=password)
#         if user:
#             login(request,user)
#             if request.GET.get(next,None):
#                 return HttpResponse(request.GET.)
#             return HttpResponse(reverce'success')
#         else:
#             context['error']='envailid u p'
#              return render(request,'home.html',context)
#     else:
#         return render(request,'home.html',context)


# class SnippetListView(ListView):
#     model = Profile
#     template_name = "employee_list.html"
#     def __init__(self, arg):
#         super(ClassName, self).__init__()
#         self.arg = arg
        


# class EmployeeListView(ListView):
#     model = Profile
#     template_name = "employee_list.html"
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['filter'] = SnippetFilter(self.request.GET, queryset=self.get_queryset())
#         return context