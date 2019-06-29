from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,AllottedLeave
from django.utils.translation import ugettext_lazy as _


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


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=10)
    last_name = forms.CharField(max_length=10)
    date_of_birth = forms.DateField(input_formats=['%Y-%m-%d'])
    date_of_joining = forms.DateField(input_formats=['%Y-%m-%d'])    
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