from django.shortcuts import render
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile



class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','password1','password2','first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('employee_id','contact_no','designation','date_of_birth','date_of_joining','teamlead',)