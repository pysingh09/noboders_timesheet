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
    path('calendar/',views.calendar, name='calendar'),
    path('show/calendar1/<int:id>',views.show_calendar,name ='show_calendar'),
    path('update/<int:id>',views.update, name='update'),
    path('employee_details/<int:id>/',views.employee_details, name='employee_details'),
    path('attendence/date-time-attendence/diff',views.date_time_attendence_view, name='date-time-attendence-view'),
    
]