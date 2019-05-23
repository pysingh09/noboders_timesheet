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
    path('edit/<int:id>/',views.edit, name='edit'),
    path('profile/',views.profile, name='profile'),
    path('profile1/',views.profile1, name='profile1'),
    path('update/<int:id>',views.update, name='update'),
    # path('person/json/', person_json, name='person_json'),
    
    path('attendence/date-time-attendence/diff',views.date_time_attendence_view, name='date-time-attendence-view'),
]