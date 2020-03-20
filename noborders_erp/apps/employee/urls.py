from employee.views import *
from django.contrib.auth.views import (
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
)
from django.urls import path, include
from django.contrib.auth import views as auth_views

app_name = "employee"


urlpatterns = [
    path("employee_wise_attendance/", emp_wise_attendance, name="employee_wise_attendance"),
    path("upload_excel/", uploadExcel, name="upload_excel"),
    path("signup/", UserCreateView.as_view(), name="signup"),
    path("home/", home, name="home"),
    path("file/", file_upload, name="file_upload"),
    path("employeelist/", EmployeeListView.as_view(), name="employee_list"),
    path("profile/", EmployeeProfile.as_view(), name="profile"),
    path("deactivate/<int:pk>/", deactivate_user, name="deactivate-user"),
    path("delete_record/", delete_record, name="delete_record"),
    path("update_leave/<int:pk>/", EditProfileView.as_view(), name="update"),
    path(
        "profile_update/<int:pk>/", EmployeeUpdateView.as_view(), name="profile_update"
    ),
    path("leave/employeelist/", LeaveListView.as_view(), name="leave_list"),
    path("profile/<int:pk>/", AllEmployeeProfile.as_view(), name="profile_list"),
    path("leaves/", LeaveCreateView.as_view(), name="leaves"),
    path("update_leave/<int:pk>/", EditAllotedLeaveView.as_view(), name="update_leave"),
    path("show/calendar/<int:id>", show_calendar, name="show_calendar"),
    path("show/calendar", show_hour_calender, name="show-hour-calender"),
    path("request/leave/", LeaveRequestView.as_view(), name="request_leave"),
    path("employee_details/<int:id>/", employee_details, name="employee_details"),
    path(
        "attendence/date-time-attendence/diff",
        date_time_attendence_view,
        name="date-time-attendence-view",
    ),
    path(
        "attendence/request/list/",
        attendence_request_list,
        name="attendence-request-list",
    ),
    path("login/", login_view, name="login"),
    path("", index, name="index"),
    path("dashboard/<int:pk>/", EmployeeProfile.as_view(), name="profile"),
    path("leave/status", LeaveStatusView.as_view(), name="approved_leave"),
    path("full/leave/status", full_leave_status, name="full-leave-status"),
    path("send/ooo", send_ooo_on_reject, name="send-ooo-on-reject"),
    path("leave", RequestLeaveView.as_view(), name="request-full-leave"),
    path("all/leave/list", AllEmpLeaveListView.as_view(), name="all-leave-list"),
    path(
        "                                                                                                                                                            leave/list",
        EmpLeaveListView.as_view(),
        name="leave-list",
    ),
    path("myleave/list", MyLiveListView.as_view(), name="my-leave-list"),
    path("fullday/leave/list", FullLeaveListView.as_view(), name="fullday-list"),
    path("team/request", InOutTimeListView.as_view(), name="in-out-request-list"),
    path("change-password/", change_password, name="change_password"),
    path("forgot-password/", ForgotPassword.as_view(), name="forgot_password"),
    # path('show-leave-list/',ShowLeaveListView.as_view(),name='show-leave-list'),
    path("delete-leave/", delete_leave, name="del-leave-list"),
    path("project_detail/", project_index, name="project-detail"),
    path("project_lead_detail/", lead_index, name="lead-detail"),
    #########
    path("create_project/", create_projectview),
    path("delete_project/<int:pk>/", project_delete_view),
    path("update_project/<int:pk>/", project_update_view),
   ######
    path("client_detail/", client_index, name="client-detail"),
    path("create_client/", create_client_view),
    path("delete_client/<int:pk>/", client_delete_view),
    path("update_client/<int:pk>/", client_update_view),
   #########
    path("assign", assign, name="assign"),
    path("assign_project/", assign_project_view, name="assign-project"),
    path("assign_project_delete/<int:pk>/", assign_delete_view),
    path("assign_project_update/<int:pk>/", assign_update_view),
    ###########
    path("daily_update/", allemployedailyupdates, name="daily-update"),
    path("employedaily_update", employedailyupdate, name="employe-dailyupdate"),
    path("check_daily_update", checkdailyupdate, name="check-daily-update"),
    path('edit_daily_update/<int:pk>/', editdailyreport, name='edit-daily-update'),
    path('delete_daily_update/<int:pk>/', deletedailyreport, name='delete-daily-update'),
    # path('search_daily_update/', searchdailyreport, name='search-daily-update'),
        # path('employe_project_update/',employeprojectupdate)
]
