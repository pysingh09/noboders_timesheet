from django import template
import datetime
from employee.models import EmployeeAttendance
from django.contrib.auth.models import User
from datetime import timedelta
register = template.Library()


@register.simple_tag()
def get_date_time_diff_tag(request, att_date,user):
	attendances_data = EmployeeAttendance.objects.filter(user=user,date=att_date)
	dateTimeDifference = datetime.timedelta(0, 0)
	for attendance in attendances_data:
		intime = attendance.in_time
		outtime = attendance.out_time
		dateTimeIn = datetime.datetime.combine(datetime.date.today(), intime)
		dateTimeOut = datetime.datetime.combine(datetime.date.today(), outtime)
		dateTimeDifference += dateTimeOut - dateTimeIn
		
	return dateTimeDifference

