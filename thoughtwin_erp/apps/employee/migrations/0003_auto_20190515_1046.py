# Generated by Django 2.0.6 on 2019-05-15 10:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_employeeattendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeattendance',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='teamlead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teamlead', to=settings.AUTH_USER_MODEL, verbose_name='Teamlead'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
