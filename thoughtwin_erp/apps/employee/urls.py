from django.urls import path
from employee.views import *
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm,    password_reset_complete
from django.urls import path, include
from django.contrib.auth import views as auth_views
app_name = 'employee'

urlpatterns = [

    path('signup/', UserCreateView.as_view(), name='signup'),
    path('home/', home, name='home'),
    path('file/', file_upload, name='file_upload'),
    path('employeelist/', EmployeeListView.as_view(), name='employee_list'),
    path('profile/', EmployeeProfile.as_view(), name='profile'),
    path('deactivate/<int:pk>/', deactivate_user,name='deactivate-user'),
    path('delete_record/', delete_record, name='delete_record'), 
    
    path('update/<int:pk>/', EditProfileView.as_view(), name="update"),
    path('profile_update/<int:pk>/', EmployeeUpdateView.as_view(), name="profile_update"),

    path('leave/employeelist/', LeaveListView.as_view(), name='leave_list'),
    path('profile/<int:pk>/', AllEmployeeProfile.as_view(), name="profile_list"),
    
    path('leaves/', LeaveCreateView.as_view(), name="leaves"),
    path('update_leave/<int:pk>/', EditAllotedLeaveView.as_view(), name="update_leave"),
    
    path('show/calendar/<int:id>', show_calendar,name ='show_calendar'),
    path('show/calendar', show_hour_calender,name ='show-hour-calender'),

    path('request/leave/', LeaveRequestView.as_view(),name ='request_leave'),
    path('employee_details/<int:id>/', employee_details, name='employee_details'),
    path('attendence/date-time-attendence/diff', date_time_attendence_view, name='date-time-attendence-view'),
    path('attendence/request/list/', attendence_request_list, name='attendence-request-list'),
    path('login/', login_view, name='login'),
    path('', index, name='index'),
    path('dashboard/<int:pk>/', EmployeeProfile.as_view(), name='profile'),
    path('leave/status', LeaveStatusView.as_view(), name='approved_leave' ),
    path('full/leave/status', full_leave_status , name='full-leave-status' ),
    path('leave', RequestLeaveView.as_view(), name='request-full-leave' ),
    path('leave/list',EmpLeaveListView.as_view(), name = 'leave-list'),
    path('fullday/leave/list', FullLeaveListView.as_view(), name = 'fullday-list'),
    path('change-password/', change_password, name='change_password'),
    path('forgot-password/', ForgotPassword.as_view(), name='forgot_password'),
    path('show-leave-list/',ShowLeaveListView.as_view(),name='show-leave-list'),
    path('delete-leave/',delete_leave,name='del-leave-list'),
  
   

     
]