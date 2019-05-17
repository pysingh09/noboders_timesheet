from django.shortcuts import render,redirect
from django.views.generic import View   #,ListView,CreateView,TemplateView,DetailView,DeleteView

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return redirect('employee:dashboard')

class Dashboard(View):
    def get(self, request):
        return render(request, 'dashboard/dashboard.html')