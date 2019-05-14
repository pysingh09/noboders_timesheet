import json
from django.shortcuts import render
from django.views.generic import View ,ListView #CreateView,TemplateView,DetailView,DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login
from employee.models import Profile     
from employee.forms import SignUpForm,ProfileForm
from django.contrib.auth.models import User
from django.http import JsonResponse


# Create your views here.
# class Dashboard(View):
#     def get(self, request):
#         return render(request, 'dashboard/dashboard.html')

@login_required
def home(request):
    return render(request,'home.html')

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


class EmployeeListView(ListView):
    model = Profile
    template_name = "employee_list.html"
    def get_context_data(self, **kwargs):
        context = super(EmployeeListView, self).get_context_data(**kwargs)
        context['emp_list'] = Profile.objects.all()
        return context

def edit(request, id):  
    employee = Profile.objects.get(id=id)  
    return render(request,'edit.html', {'employee':employee})

def update(request, id):  
    employee = Profile.objects.get(id=id)  
    form = ProfileForm(request.POST, instance = employee)  
    if form.is_valid():  
        form.save() 
        return redirect("/employee_list.html")  
    return render(request, 'edit.html', {'employee': employee})

def person_json(request):
    persons = Profile.objects.all()
    data = [person.to_dict_json() for person in persons]
    result = {'data': data}
    response = json.dumps(list(result)) 
    return JsonResponse(response,safe=False)






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