from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Create Pre-defined Roles and Permissions'

    def handle(self, *args, **options):

        predefined_roles = ['MD','Project Manager','BDE','HR','TeamLead','Trainee','QA','Senior Developer','Junior Developer']
        for role in predefined_roles:
            group, created = Group.objects.get_or_create(name=role)
            
        self.stdout.write(self.style.SUCCESS('Successfully Done'))