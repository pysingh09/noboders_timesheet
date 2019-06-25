from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile,EmployeeAttendance,AllottedLeave,EmployeeAttendanceDetail,FulldayLeave

class EmployeeAttendanceModelAdmin(admin.ModelAdmin):
    list_display = ( 'user_obj', 'employee_id', 'date')

    def user_obj(request, obj):
        return obj.user.username
    
admin.site.register(Profile)
admin.site.register(EmployeeAttendance, EmployeeAttendanceModelAdmin)
admin.site.register(AllottedLeave)
admin.site.register(EmployeeAttendanceDetail)
admin.site.register(FulldayLeave)
