import json,csv,io
from django.shortcuts import render,get_list_or_404, get_object_or_404
from django.views.generic import View,ListView,TemplateView #CreateView,,DetailView,DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login
from employee.models import Profile, EmployeeAttendance
from employee.forms import SignUpForm,ProfileForm
from django.contrib.auth.models import User
from django.http import JsonResponse


# Create your views here.
# class Dashboard(View):
#     def get(self, request):
#         return render(request, 'dashboard/dashboard.html')

# @login_required
# def home(request):
#     return render(request,'home.html')

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
    template_name = "home.html"
    return render(request,template_name)


class EmployeeListView(ListView):
    model = Profile
    template_name = "employee_list.html"


def employee_data_table(request):
    persons = Profile.objects.all()
    data = [person.to_dict_json() for person in persons]
    result = {'data': data}
    response = json.dumps(list(result)) 
    return JsonResponse(response,safe=False)
        
def edit(request, id):  
    employee = Profile.objects.get(id=id)  
    return render(request,'edit.html', {'employee':employee})

def update(request, id):  
    employee = Profile.objects.get(id=id)  
    form = ProfileForm(request.POST, instance = employee) 
    # user_form = SignUpForm(request.POST, instance = employee) 
    import pdb; pdb.set_trace()
    if form.is_valid():  
        form.save() 
        return redirect("EmployeeListView")  
    return render(request, 'edit.html', {'form': form})
 

# def update(request, id, template_name='employee_list.html'):
#     book= get_object_or_404(Profile, id=id)
#     form = ProfileForm(request.POST or None, instance=book)
#     if form.is_valid():
#         form.save()
#         return redirect('employee_list.html')
#     return render(request, template_name, {'form':form})



# def update(request, id):  
#     employee = Profile.objects.get(id=id)
#     form = ProfileForm(request.POST or None, instance = employee)
#     # import pdb; pdb.set_trace()
#     if request.method == 'POST':
#         if form.is_valid():  
#             form.save()  
#             return redirect("employee_list.html")  
#     return render(request, 'edit.html', {'form': form})  



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

@login_required
def home(request):
    context = {}
    # context['user'] = request.user
    if request.user.is_superuser:
        context['attendance_data'] = EmployeeAttendance.objects.all()
    else:
        usr = User.objects.get(id = request.user.id)
        context['attendance_data'] = EmployeeAttendance.objects.filter(employee_id=usr.profile.employee_id)
    return render(request,'home.html', context)

def profile(request):
    template_name = "profile.html"
    return render(request,template_name)
    

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