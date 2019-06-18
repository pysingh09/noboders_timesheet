from django.urls import path
from employee.views import *
app_name = 'employee'

urlpatterns = [

    path('signup/', signup, name='signup'),
    path('home/', home, name='home'),
    path('file/', file_upload, name='file_upload'),
    path('employeelist/', EmployeeListView.as_view(), name='employee_list'),
    path('profile/', EmployeeProfile.as_view(), name='profile'),
    path('deactivate/<int:pk>/', deactivate_user,name='deactivate-user'),
    path('delete_record/', delete_record, name='delete_record'), 
    path('update/<int:pk>/', EditProfileView.as_view(), name="update"),
    path('leave/employeelist/', LeaveListView.as_view(), name='leave_list'),
    path('profile/<int:pk>/', ListOfProfile.as_view(), name="profile_list"),
    
    path('leaves/', LeaveCreateView.as_view(), name="leaves"),
    path('update_leave/<int:pk>/', EditAllotedLeaveView.as_view(), name="update_leave"),
    
    path('show/calendar/<int:id>', show_calendar,name ='show_calendar'),
    path('show/calendar', show_hour_calender,name ='show-hour-calender'),

    path('request/leave/', request_leave,name ='request_leave'),
    path('employee_details/<int:id>/', employee_details, name='employee_details'),
    path('attendence/date-time-attendence/diff', date_time_attendence_view, name='date-time-attendence-view'),
    path('attendence/request/list/', attendence_request_list, name='attendence-request-list'),
    path('login/', login_view, name='login'),
    path('', index, name='index'),
    path('dashboard', Dashboard.as_view(), name='dashboard' ),
    path('approved/leave', approved_leave, name='approved_leave' ),
    


]