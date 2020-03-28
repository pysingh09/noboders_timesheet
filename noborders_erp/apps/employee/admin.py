from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import (
    MonthlyTakeLeave,
    Profile,
    EmployeeAttendance,
    AllottedLeave,
    EmployeeAttendanceDetail,
    Leave,
    LeaveDetails,
    Client,
    Project,
    AssignProject,
    EmployeeDailyUpdate
)
# admin.site.register(SignUp)
admin.site.register(Profile)
admin.site.register(EmployeeAttendance)
admin.site.register(AllottedLeave)
admin.site.register(EmployeeAttendanceDetail)
admin.site.register(Leave)
admin.site.register(LeaveDetails)
admin.site.register(MonthlyTakeLeave)
admin.site.register(Client)
admin.site.register(Project)
admin.site.register(AssignProject)
admin.site.register(EmployeeDailyUpdate)

#admin.site.register(EmployeeTotalAttendanceStatus)
