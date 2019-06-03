from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User,Group
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from datetime import datetime, date
import datetime

ROLE_CHOICES = (
    (1, ('MD')),
    (2, ('Project manager')),
    (3, ('BDE')),
    (4 , ('HR')),
    (5 , ('TeamLead')),
    (6 , ('Senior developer')),
    (7 , ('Junior developer')),
    (8 , ('Trainee')),
    (9 , ('QA')),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    employee_id = models.IntegerField(unique=True, verbose_name=_('Employee ID'))
    contact_no = models.CharField(max_length=10,default=0, blank=True, verbose_name=_('Contact No'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('Date Of Birth'))
    date_of_joining = models.DateField(null=True, blank=True, verbose_name=_('Date Of Joining'))

    teamlead = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Teamlead'), related_name='teamlead')
    designation = models.IntegerField(choices=ROLE_CHOICES, default=7, verbose_name=_('Designation'))

    # teamlead = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Teamlead'))
    # designation = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name=_('Designation'))
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_created')

    def __str__(self):

        return self.user.username


class EmployeeAttendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_user')
    employee_id = models.IntegerField(verbose_name=_('Employee ID'))
    in_time = models.TimeField(blank=True, verbose_name=_('Time In'))      
    out_time = models.TimeField(blank=True, verbose_name=_('Time Out'))
    date = models.DateField(blank=True, verbose_name=_('Date'))
    total_working_time = models.FloatField(default=0)
    
    def __str__(self):
        return str(self.employee_id)


    def emp_hour(self):
        return (datetime.datetime.combine(date.today(), self.out_time) - datetime.datetime.combine(date.today(), self.in_time)).seconds / 3600

    def time_diff(self,dt):
        intime = self.in_time
        outtime = self.out_time
        dateTimeIn = datetime.datetime.combine(datetime.date.today(), intime)
        dateTimeOut = datetime.datetime.combine(datetime.date.today(), outtime)
        dateTimeDifference = dateTimeOut - dateTimeIn
        return dateTimeDifference





