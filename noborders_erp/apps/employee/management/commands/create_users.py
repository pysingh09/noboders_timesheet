from ...models import Profile
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Total number of users to be added')

    def handle(self, *args, **options):
        total = options['total']
        #for i in range(total):
        name = input('Enter username\n')
        emp_id = input('Enter user id\n')

        del_user = User.objects.filter(username=name)
        del_user.delete()
            # User.objects.create_user(username=name, email='', password=name+'@1234')
            # user = User.objects.get_by_natural_key(username=name)
            # team_lead = Profile.objects.get(designation="TeamLead")
            # Profile.objects.update_or_create(user=user, employee_id=emp_id, contact_no='',
            #                                  date_of_birth=None, date_of_joining=None, teamlead=team_lead,
            #                                  working_time="9:00", created_by=team_lead)