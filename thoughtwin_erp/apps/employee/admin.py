from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Profile,EmployeeAttendance,LeaveRequest
User = get_user_model()


admin.site.register(Profile)
admin.site.register(EmployeeAttendance)
admin.site.register(LeaveRequest)
