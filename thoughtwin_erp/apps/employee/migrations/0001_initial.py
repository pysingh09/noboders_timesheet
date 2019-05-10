# Generated by Django 2.0.6 on 2019-05-10 08:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField(unique=True, verbose_name='Employee ID')),
                ('contact_no', models.CharField(blank=True, default=0, max_length=10, verbose_name='Contact No')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date Of Birth')),
                ('date_of_joining', models.DateField(blank=True, null=True, verbose_name='Date Of Joining')),
                ('designation', models.IntegerField(choices=[(1, 'MD'), (2, 'Project manager'), (3, 'BDE'), (4, 'HR'), (5, 'TeamLead'), (6, 'Senior developer'), (7, 'Junior developer'), (8, 'Trainee'), (9, 'QA')], default=7, verbose_name='Designation')),
                ('teamlead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Teamlead')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
