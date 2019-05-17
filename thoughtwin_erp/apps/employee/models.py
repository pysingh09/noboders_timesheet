from django.db import models
from django.conf import settings
from django.contrib.auth.models import User,Group
from django.utils.translation import ugettext_lazy as _

# Create your models here.
# ROLE_CHOICES = (
#         (1, ('MD')),
#         (2, ('Project manager')),
#         (3, ('BDE')),
#         (4 , ('HR')),
#         (5 , ('TeamLead')),
#         (6 , ('Senior developer')),
#         (7 , ('Junior developer')),
#         (8 , ('Trainee')),
#         (9 , ('QA')),
#     )

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    employee_id = models.IntegerField(unique=True, verbose_name=_('Employee ID'))
    contact_no = models.CharField(max_length=10,default=0, blank=True, verbose_name=_('Contact No'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('Date Of Birth'))
    date_of_joining = models.DateField(null=True, blank=True, verbose_name=_('Date Of Joining'))
    teamlead = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Teamlead'))
    designation = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name=_('Designation'))
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_created')

    def __str__(self):    

        return self.user.username

# class Employee_Attendance(models.Model):
#     employee_no = models.IntegerField(verbose_name=_('Employee Number'))
#     in_time = models.TimeField(blank=True, verbose_name=_('Time In'))      
#     out_time = models.TimeField(blank=True, verbose_name=_('Time out'))
#     date = models.DateField(blank=True, verbose_name=_('Date'))
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     # total_working_hours = models.TimeField(blank=True)
   
#     def __str__(self):
#         return str(self.employee_no)