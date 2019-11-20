from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User,Group
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum
from datetime import datetime, date
import datetime
# from phonenumber_field.modelfields import PhoneNumberField

LEAVE_CHOICES = []
for r in range(2019, (datetime.datetime.now().year+10)):
   LEAVE_CHOICES.append((r,r))
MONTH_CHOICES = (
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11,'November'),
    (12,'December'),

    )

LEAVE_STATUS = (
    (1, 'Pending'),
    (2, 'Accepted'),
    (3, 'Rejected'),
    )

LEAVE_TYPE = (
    (1, 'Default'),
    (2, 'Half day'),
    (3, 'Full day'),
    )

EMPATT_LEAVE_STATUS = (
    (1, 'Default'),
    (2, 'Request by employee'),
    (3, 'Accepted'),
    (4, 'Rejected'),

    (5, 'Pending'),
    (6, 'Accepted'),
    (7, 'Rejected'),
    )

ROLE_CHOICES = ( 
    (1, ('MD')),
    (2, ('Project Manager')),
    (3, ('BDE')),
    (4 , ('HR')),
    (5 , ('TeamLead')),
    (6 , ('Trainee')),
    (7 , ('QA')),
    (8 , ('Senior Developer')),
    (9 , ('Junior Developer')),  
)

class BaseModel(models.Model):
   created_at = models.DateTimeField(auto_now_add=True, db_index=True)
   modified_at = models.DateTimeField(auto_now=True, db_index=True)

   class Meta:
       abstract = True        

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    employee_id = models.IntegerField(unique=True, verbose_name=_('Employee ID'))
    contact_no = models.CharField(max_length=10)
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('Date Of Birth'))
    date_of_joining = models.DateField(null=True, blank=True, verbose_name=_('Date Of Joining'))
    profile_image = models.ImageField(upload_to = 'pic_folder/', default = 'avatar-mini-2.jpg')
    teamlead = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Teamlead'), related_name='teamlead')
    designation = models.IntegerField(choices=ROLE_CHOICES, default=7, verbose_name=_('Designation'))

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_created_by')

    def __str__(self):

        return self.user.username
    
    class Meta:
        permissions = (
            ("can_view_user_profile_list", "Can View User Profile List"),
        )
     

    def get_leave(self):
          return self.user.user_leaves.get(user=self.user, year=datetime.datetime.now().year).leave

    def get_leave(self):
        try:
            return self.user.user_leaves.filter(user=self.user, year=datetime.datetime.now().year).aggregate(Sum('leave'))['leave__sum']-self.user.employee_user.filter(empatt_leave_status__in =['6']).aggregate(Sum('leave_day_time'))['leave_day_time__sum']
        except Exception as e:
             return self.user.user_leaves.filter(user=self.user, year=datetime.datetime.now().year).aggregate(Sum('leave'))['leave__sum']

    @property
    def full_name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


class EmployeeAttendance(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_user')
    employee_id = models.IntegerField(verbose_name=_('Employee ID'))
    date = models.DateField(blank=True, verbose_name=_('Date'))
    leave_type = models.IntegerField(choices=LEAVE_TYPE, default=1)
    empatt_leave_status = models.IntegerField(choices=EMPATT_LEAVE_STATUS, default=1)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True , related_name='attendance_created_by')
    leave_day_time = models.FloatField(default=0)
 

    class Meta:
        unique_together = ('user', 'date',)

    class Meta:
        permissions = (
            ("can_view_employee_attendance_list", "Can View Employee Attendance List"),
        )

    def __str__(self):
        return str(self.employee_id)


    def date_time_diffrence(self):
        dateTimeDifference = datetime.timedelta(0, 0)
        for emp_detail in self.employee_attendance.all():
            intime = emp_detail.in_time
            outtime = emp_detail.out_time
            dateTimeIn = datetime.datetime.combine(datetime.date.today(), intime)
            dateTimeOut = datetime.datetime.combine(datetime.date.today(), outtime)
            dateTimeDifference += dateTimeOut - dateTimeIn
        return dateTimeDifference
        

class AllottedLeave(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_leaves')
    year = models.IntegerField(choices=LEAVE_CHOICES, verbose_name=_('Year'))
    month = models.IntegerField(choices=MONTH_CHOICES, verbose_name=_('Month'))

    leave = models.FloatField(default=0,verbose_name=_('Leaves'))
    bonusleave = models.FloatField(default=0,verbose_name=_('Bonus Leave'))
    available_bonus_leave = models.FloatField(default=0,verbose_name=_('Available Bonus Leave'))
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='leave_created_by')
    
    def total_allotted_leave(self):
        return self.leave + self.bonusleave

    class Meta:
        unique_together = ('year', 'user',)

    def __str__(self):
        return self.user.username + " : " + str(self.leave + self.bonusleave - self.available_bonus_leave )


    def get_full_leave(self):
        return self.user.user_leaves.filter(user=self.user, year=datetime.datetime.now().year).aggregate(Sum('leave'))['leave__sum']
        try:
            return self.user.user_leaves.filter(user=self.user, year=datetime.datetime.now().year).aggregate(Sum('leave'))['leave__sum'] - self.user.employee_user.filter(empatt_leave_status__in =['6']).aggregate(Sum('leave_day_time'))['leave_day_time__sum']
        except Exception as e:
             return self.user.user_leaves.filter(user=self.user, year=datetime.datetime.now().year).aggregate(Sum('leave'))['leave__sum']

class EmployeeAttendanceDetail(models.Model):
    employee_attendance = models.ForeignKey(EmployeeAttendance, on_delete=models.CASCADE, related_name='employee_attendance')
    in_time = models.TimeField(blank=True, verbose_name=_('Time In')) 
    out_time = models.TimeField(blank=True, verbose_name=_('Time Out'))


    def date_time_diffrence(self):
        dateTimeDifference = datetime.timedelta(0, 0)
        dateTimeIn = datetime.datetime.combine(datetime.date.today(), self.in_time)
        dateTimeOut = datetime.datetime.combine(datetime.date.today(), self.out_time)
        dateTimeDifference = dateTimeOut - dateTimeIn
        return dateTimeDifference

class Leave(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fullday_leave_user')
    startdate = models.DateField(verbose_name=_('Start Date'))
    enddate = models.DateField(verbose_name=_('End Date'))
    starttime = models.TimeField(null=True,blank=True, verbose_name=_('Time In')) 
    endtime = models.TimeField(null=True,blank=True, verbose_name=_('Time Out'))
    leave_type = models.IntegerField(choices=LEAVE_TYPE)
    status = models.IntegerField(choices=LEAVE_STATUS, default=1)
    is_ooo_send = models.BooleanField(default=False)
 
    def __str__(self):
        return self.user.username

class LeaveDetails(models.Model):
    leave = models.ForeignKey(Leave, on_delete=models.CASCADE, related_name='leavedetails')
    reason = models.TextField(null=True)
    status = models.IntegerField(choices=LEAVE_STATUS, default=1)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='leave_detail_created_by')

LEAVE_MONTH_STATUS_CHOICES =((1, 'Paid'),(2, 'Unpaid'),)
class MonthlyTakeLeave(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_take_leaves')
    year = models.IntegerField(choices=LEAVE_CHOICES, verbose_name=_('Year'))
    month = models.IntegerField(choices=MONTH_CHOICES, verbose_name=_('Month'))
    leave = models.FloatField(default=0,verbose_name=_('Leaves'))
    status = models.IntegerField(choices=LEAVE_MONTH_STATUS_CHOICES,default=1,verbose_name=_('Leave Status'))
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='monthy_leave_created_by')    