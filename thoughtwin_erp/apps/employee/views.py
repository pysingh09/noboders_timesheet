from django.shortcuts import render,redirect
from django.views.generic import View   #,ListView,CreateView,TemplateView,DetailView,DeleteView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import login, logout
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