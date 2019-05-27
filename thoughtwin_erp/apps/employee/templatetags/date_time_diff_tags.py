from django import template
import datetime
from employee.models import EmployeeAttendance
register = template.Library()


# in complete admin

@register.simple_tag()
def get_date_time_diff_tag(request, att_date):
	if request.user.is_superuser:
		# name = EmployeeAttendance.objects.get(employee_id="employee_id")
		# recipe = EmployeeAttendance.objects.get(employee_id="employee_id")
		attendances_data = EmployeeAttendance.objects.all()
		
		for attendance in attendances_data:
			dateTimeDifference = datetime.timedelta(0, 0)
			# import pdb; pdb.set_trace()
			user_data = attendances_data.filter(user=attendance.user, date = attendance.date)
			for users_data in user_data:
				intime = users_data.in_time
				outtime = users_data.out_time
				# print(users_data)
				dateTimeIn = datetime.datetime.combine(datetime.date.today(), intime)
				dateTimeOut = datetime.datetime.combine(datetime.date.today(), outtime)
				dateTimeDifference += dateTimeOut - dateTimeIn
				print(dateTimeDifference)
			# intime = attendance.in_time
			# outtime = attendance.out_time
			# dateTimeIn = datetime.datetime.combine(datetime.date.today(), intime)
			# dateTimeOut = datetime.datetime.combine(datetime.date.today(), outtime)
			# dateTimeDifference += dateTimeOut - dateTimeIn
			# print(dateTimeDifference)
		return dateTimeDifference
		# attendances_data = EmployeeAttendance.objects.all()
		
		# time_defference = []
		# # import pdb; pdb.set_trace()
		# for attendance in attendances_data:
		# 	intime = attendance.in_time
		# 	outtime = attendance.out_time
		# 	dateTimeIn = datetime.datetime.combine(datetime.date.today(), intime)
		# 	dateTimeOut = datetime.datetime.combine(datetime.date.today(), outtime)
		# 	# import pdb; pdb.set_trace()
		# 	dateTimeDifference= dateTimeOut - dateTimeIn

		# 	time_defference.append(dateTimeDifference)

		# return time_defference

	else:

		attendances_data = EmployeeAttendance.objects.filter(user=request.user,date=att_date)
		# import pdb; pdb.set_trace()
		dateTimeDifference = datetime.timedelta(0, 0)
		for attendance in attendances_data:
			intime = attendance.in_time
			outtime = attendance.out_time
			dateTimeIn = datetime.datetime.combine(datetime.date.today(), intime)
			dateTimeOut = datetime.datetime.combine(datetime.date.today(), outtime)
			dateTimeDifference += dateTimeOut - dateTimeIn
		return dateTimeDifference