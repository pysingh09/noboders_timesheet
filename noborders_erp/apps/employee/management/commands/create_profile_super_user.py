from ...models import Profile
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

"""
This scripts is a management command used for creating 
admin user/ super user and add that user in profile table

Run this script with following command:-

./manage.py create_profile_super_user
"""


class Command(BaseCommand):

    def handle(self, *args, **options):
        user_name = input("Please enter username:  ")
        email = input("Please enter email address:  ")
        password = input("Please enter password:  ")
        confirm_password = input("Please re-enter password to confirm:  ")

        if password == confirm_password:
            user = User.objects.create_user(username=user_name, email=email, password=password)

            user.is_superuser = True
            user.is_active = True
            user.is_admin = True
            user.is_staff = True
            user.save()
            contact_number = input("Please enter contact number: ")
            Profile.objects.update_or_create(user=user,
                                             employee_id='112',
                                             contact_no=contact_number,
                                             teamlead=user,
                                             created_by=user)

        else:
            raise Exception("Password and Confirm password didn't match")
