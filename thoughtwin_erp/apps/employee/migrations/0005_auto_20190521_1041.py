# Generated by Django 2.0.6 on 2019-05-21 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_auto_20190515_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeattendance',
            name='total_working_time',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='employeeattendance',
            name='out_time',
            field=models.TimeField(blank=True, verbose_name='Time Out'),
        ),
    ]
