from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.task import periodic_task
from celery.utils.log import get_task_logger
from datetime import timedelta, datetime
from employee.models import Leave, User, LeaveDetails
from django.core.mail import EmailMessage,send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

logger = get_task_logger(__name__)

# Gets weather data from Darksky API (third-party api)
@periodic_task(run_every=(crontab(minute=30, hour=14)), name="send_email_reminder", ignore_result=True)
def send_email_reminder():
    print('aaaaaaaa')
    send_email_reminder_method()

# @periodic_task(run_every=timedelta(seconds=2), name="get_weather_data_for_store_task", ignore_result=True)

def send_email_reminder_method():
    objects = Leave.objects.filter(startdate=datetime.now(), status=2)
    print('bbbbbbbbb')
    if objects != []:
        print('cccccccccccc')
        for obj in objects:
            if obj.is_ooo_send == False:
                leavedetail = LeaveDetails.objects.filter(leave=obj).first()
                startdate = obj.startdate.strftime("%b %d, %Y")
                enddate = obj.enddate.strftime("%b %d, %Y") 
                if obj.leave_type == 2:
                    email_subject = "OOO ||"" "+obj.user.profile.full_name+" "'||'" "+obj.get_leave_type_display()+" "'||'" "+startdate
                    content = render_to_string('email/ooo_email_content.html',{'user':obj.user,'startdate':startdate,'reason':leavedetail.reason  })
                if obj.leave_type == 3:
                    email_subject = "OOO ||"" "+obj.user.profile.full_name+" "'||'" "+obj.get_leave_type_display()+" "'||'" "+startdate+"-"+enddate
                    content = render_to_string('email/ooo_email_content.html',{'user':obj.user.profile.full_name,'startdate':obj.startdate,'enddate':obj.enddate,'reason':leavedetail.reason})
                text_content = strip_tags(content)
            for user in User.objects.all():
                try:
                    msg = EmailMultiAlternatives(email_subject, text_content, settings.FROM_EMAIL, [user.email])
                    msg.attach_alternative(content, "text/html")
                    print("send OOO on  " + user.email)
                    msg.send()
                    objects.is_ooo_send = True
                    objects.save()
                except Exception as e:
                    pass