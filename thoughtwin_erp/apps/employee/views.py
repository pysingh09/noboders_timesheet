import json,csv,io
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.generic import View,ListView,TemplateView,UpdateView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login
from employee.models import Profile, EmployeeAttendance
from employee.forms import SignUpForm,ProfileForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


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
            return redirect("/emplist/")
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
    success_url = "/emplist/"
    def get_object(self, *args, **kwargs):
        profile_obj = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return  profile_obj


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
        # import pdb; pdb.set_trace()
        in_time1= datetime.strptime(column[1], "%I:%M%p")
        out_time1= datetime.strptime(column[2], "%I:%M%p")
        _, created= EmployeeAttendance.objects.update_or_create(
            user=profile.user,
            employee_id = column[0],
            in_time = in_time1,
            out_time =out_time1,
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