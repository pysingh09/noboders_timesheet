from django.urls import path
from employee.views import * 
from . import views
app_name = 'employee'

urlpatterns = [
    # path('dashboard', Dashboard.as_view(), name='dashboard' ),
    path('signup/', signup, name='signup'),
    path('home/', home, name='home'),
    path('file/', file_upload, name='file_upload'),
    path('emplist/', views.EmployeeListView.as_view(), name='employee_list'),
    path('edit/<int:id>/', edit, name='edit'),
    path('update/<int:id>', update, name='update'),
    # path('person/json/', person_json, name='person_json'),


]