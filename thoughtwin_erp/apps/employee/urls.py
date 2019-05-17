from django.urls import path
from .views import *
app_name = 'employee'

urlpatterns = [
    path('', index, name='index'),
    path('dashboard', Dashboard.as_view(), name='dashboard' ),
]