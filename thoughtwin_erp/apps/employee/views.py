from django.shortcuts import render
from django.views.generic import View   #,ListView,CreateView,TemplateView,DetailView,DeleteView

# Create your views here.
class Dashboard(View):
    def get(self, request):
        return render(request, 'dashboard/dashboard.html')