from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,AllottedLeave,Leave
from django.utils.translation import ugettext_lazy as _
from django.contrib import auth
from django.forms import ValidationError
from django.contrib.auth.password_validation import CommonPasswordValidator
# from phonenumber_field.formfields import PhoneNumberField

# class SignUpForm(forms.ModelForm):
#     username = forms.CharField(max_length=30)
#     first_name = forms.CharField(max_length=30)
#     last_name = forms.CharField(max_length=30)
#     email = forms.EmailField(max_length=254)
#     class Meta:
#         model = SignUp
#         fields = ('username','password1','password2','first_name', 'last_name', 'email')

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         username = self.cleaned_data.get('username')
#         if email and SignUp.objects.filter(email=email).exclude(username=username).exists():
#             raise forms.ValidationError('Email address already exist.')
#         return email

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','password1','password2','first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email address already exist.')
        return email
    # def clean(self):
       
    #     # super(SignUpForm, self).clean()
    #    # This method will set the `cleaned_data` attribute
    #     password1 = self.cleaned_data.get('password1')
    #    # re_password = self.cleaned_data.get('password2')
    #     if CommonPasswordValidator().validate(password1):
    #         raise forms.ValidationError("Please choose another password")
    #     return password1
       # if not password == re_password:
       #     raise ValidationError('Passwords must match')
    # def clean_password1(self):
    #     import pdb; pdb.set_trace()
    #     validate_password(self.cleaned_data.get('password1'))
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
# class EmployeeRegistrationForm(UserCreationForm):
#     employee_id = forms.CharField(max_length=10)
#     contact_no = forms.CharField(max_length=10)        
#     date_of_birth = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
#     date_of_joining = forms.DateField(help_text='Required. Format: YYYY-MM-DD') 
#     designation = forms.ChoiceField(choices = ROLE_CHOICES)
#     teamlead = forms.ModelChoiceField(queryset=User.objects.all())
#     class Meta:
#         model = User
#         fields = ('first_name','last_name','email','password1','password2')   

class UserProfileForm(forms.ModelForm):
    employee_id = forms.CharField(max_length=10)

    # contact_no = PhoneNumberField(widget=forms.TextInput(attrs={'value': _('+91')}), 

    #                    label=_("Phone number"), required=True)
    class Meta:
        model = Profile
        fields = ('contact_no','designation','date_of_birth','date_of_joining','teamlead',)    
    

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=10)
    last_name = forms.CharField(max_length=10)
    date_of_birth = forms.DateField(input_formats=['%Y-%m-%d'])
    date_of_joining = forms.DateField(input_formats=['%Y-%m-%d'])
    contact_no = forms.IntegerField()
    class Meta:
        model = Profile
        fields = ('employee_id','contact_no','designation','date_of_birth','date_of_joining','teamlead', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ProfileForm, self).__init__(*args, **kwargs)
        # if you want to admin can not update employee_id so uncomment both lines which are commented
        
        # self.fields['employee_id'].required = False 
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            # self.fields['employee_id'].widget.attrs['readonly'] = True
            self.fields['first_name'].initial = instance.user.first_name
            self.fields['last_name'].initial = instance.user.last_name  

class AllottedLeavesForm(forms.ModelForm):

    class Meta:
        model = AllottedLeave
        fields = ['user','year','leave']

import datetime as dt

HOUR_CHOICES = []
for x in range(1,24):
    y=x
    fmt = 'AM'
    if x == 12:
        fmt = 'PM' 
    if x >= 13:
       y = x-12
       fmt = 'PM' 
    x = str(x)
    y = str(y)

    HOUR_CHOICES.append((x+':00',y+':00 '+fmt))
    HOUR_CHOICES.append((x+':30',y+':30 '+fmt))

class LeaveCreateForm(forms.ModelForm):
    leave_type = forms.ChoiceField(choices=[('', '----'),(2, 'Half Day'),(3, 'Full Day'),])
    reason = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':4}))
    starttime = forms.ChoiceField(required=False,choices=HOUR_CHOICES)
    endtime = forms.ChoiceField(required=False,choices=HOUR_CHOICES)
    class Meta:
        model = Leave
        fields = ('startdate','enddate')


class changePassForm(forms.Form):
    old_password_flag = True #Used to raise the validation error when it is set to False

    old_password = forms.CharField(label="Old Password", min_length=6, widget=forms.PasswordInput())
    new_password = forms.CharField(label="New Password", min_length=6, widget=forms.PasswordInput())
    re_new_password = forms.CharField(label="Confirm Password", min_length=6, widget=forms.PasswordInput())

    def set_old_password_flag(self): 
        self.old_password_flag = False
        return 0

    def clean_old_password(self, *args, **kwargs):
        old_password = self.cleaned_data.get('old_password')
        if not old_password:
            raise forms.ValidationError("You must enter your old password.")

        if self.old_password_flag == False:
            raise forms.ValidationError("The old password that you have entered is wrong.")
        return old_password

class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=10)
    last_name = forms.CharField(max_length=10)
    class Meta:
        model = Profile
        fields = ('contact_no','first_name', 'last_name','profile_image')
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        # if you want to admin can not update employee_id so uncomment both lines which are commented
        
        # self.fields['employee_id'].required = False 
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            # self.fields['employee_id'].widget.attrs['readonly'] = True
            self.fields['first_name'].initial = instance.user.first_name
            self.fields['last_name'].initial = instance.user.last_name  