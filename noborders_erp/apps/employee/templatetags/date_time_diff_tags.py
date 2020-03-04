from django import template
import datetime
from employee.models import EmployeeAttendanceDetail
from django.contrib.auth.models import User
from datetime import timedelta
register = template.Library()


# @register.simple_tag()
# def get_date_time_diff_tag(request, att_date,user):
# 	import pdb; pdb.set_trace()
# 	attendances_data = EmployeeAttendanceDetail.objects.filter(user=user,date=att_date)
# 	dateTimeDifference = datetime.timedelta(0, 0)
# 	for attendance in attendances_data:
# 		intime = attendance.in_time
# 		outtime = attendance.out_time
# 		dateTimeIn = datetime.datetime.combine(datetime.date.today(), intime)
# 		dateTimeOut = datetime.datetime.combine(datetime.date.today(), outtime)
# 		dateTimeDifference += dateTimeOut - dateTimeIn
		
# 	return dateTimeDifference
@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
