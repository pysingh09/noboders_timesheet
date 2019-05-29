from django.shortcuts import render
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.utils.translation import ugettext_lazy as _


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username','password1','password2','first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'This Email address allready exist.')
        return email


class ProfileForm(forms.ModelForm):
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
    designation = forms.IntegerField(widget=forms.Select(choices=ROLE_CHOICES))
    class Meta:
        model = Profile
        fields = ('employee_id','contact_no','designation','date_of_birth','date_of_joining','teamlead',)