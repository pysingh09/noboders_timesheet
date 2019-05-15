from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save


# Create your models here.
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

    def __str__(self):  
        return self.user.username

# def create_profile(sender , **kwargs):
#     user= kwargs['instance']
#     if kwargs['created']:
#         user_profile = Profile(user=user)
#         user_profile.save()
#         post_save.connect(create_profile, sender=User) 

class EmployeeAttendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_user')
    employee_id = models.IntegerField(verbose_name=_('Employee ID'))
    in_time = models.TimeField(blank=True, verbose_name=_('Time In'))      
    out_time = models.TimeField(blank=True, verbose_name=_('Time out'))
    date = models.DateField(blank=True, verbose_name=_('Date'))
    # total_working_hours = models.TimeField(blank=True)
    def __str__(self):
        return str(self.employee_id)







    # def to_dict_json(self):
    #     return {
    #         'user': self.user,
    #         'employee_id': self.employee_id,
    #         'contact_no': self.contact_no,
    #         'designation': self.designation,
        


