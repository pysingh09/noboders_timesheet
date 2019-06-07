from django.urls import path
from employee.views import *
app_name = 'employee'

urlpatterns = [

    path('signup/', signup, name='signup'),
    path('home/', home, name='home'),
    path('profile/', employee_profile, name='profile'),
    path('file/', file_upload, name='file_upload'),
    path('employeelist/', EmployeeListView.as_view(), name='employee_list'),
    path('profile/', employee_profile, name='profile'),
    path('deactivate/<int:pk>/', deactivate_user,name='deactivate-user'),
    path('delete_record/', delete_record, name='delete_record'), 
    path('update/<int:pk>/', EditProfileView.as_view(), name="update"),
    path('calendar/', calendar, name='calendar'),
    path('show/calendar1/<int:id>', show_calendar,name ='show_calendar'),
    # path('home/', home, name='home'),
    path('show/', show,name ='calendar'),
    path('employee_details/<int:id>/', employee_details, name='employee_details'),
    path('attendence/date-time-attendence/diff', date_time_attendence_view, name='date-time-attendence-view'),
    
    path('login/', login_view, name='login'),
    path('', index, name='index'),
    path('dashboard', Dashboard.as_view(), name='dashboard' ),

]