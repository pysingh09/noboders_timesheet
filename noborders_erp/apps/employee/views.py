import json, csv, io
from datetime import datetime, date, timedelta, tzinfo, timezone
import datetime as only_datetime
from dateutil import relativedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic import View, ListView, TemplateView, UpdateView, DetailView
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.generic import View, ListView, TemplateView, CreateView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.forms import ValidationError


from employee.models import (
    MonthlyTakeLeave,
    Profile,
    EmployeeAttendance,
    AllottedLeave,
    EmployeeAttendanceDetail,
    Leave,
    LeaveDetails,
    Project,
    Client,
    AssignProject,
    EmployeeDailyUpdate,
)
from employee.forms import (
    SignUpForm,
    ProfileForm,
    AllottedLeavesForm,
    LeaveCreateForm,
    UserProfileForm,
    changePassForm,
    ProfileEditForm,
    CustomAuthForm,
    ProjectForm,
    ClientForm,
    AssignForm,
    EmployeeDailyUpdateForm,
    EditDailyUpdateForm,
)

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Count
from time import sleep
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.views import login, logout
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.dateparse import parse_date
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned

# permission
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.template import loader
from django.contrib.auth.models import Group

from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from employee.tasks import send_email_reminder

# this is for file upload
import xlrd
from django.conf import settings
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage()


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = CustomAuthForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect("employee:profile")
            else:
                return render(request, "registration/login.html", {"form": form})
        else:
            form = CustomAuthForm()
            messages.error(request, "")
        return render(request, "registration/login.html", {"form": form})
    else:
        return redirect("employee:profile")


def index(request):
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        return redirect("employee:profile")


class UserCreateView(PermissionRequiredMixin, CreateView):

    permission_required = ("employee.add_profile",)
    raise_exception = True
    form_class = SignUpForm
    second_form_class = ProfileForm
    template_name = "registration/signup.html"
    success_url = "/employeelist/"

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        if "form2" not in context:
            context["form2"] = self.second_form_class()
        return context

    def form_invalid(self, form, **kwargs):

        # context['form'] = super().form_invalid(form)
        context = self.get_context_data(**kwargs)
        context["form2"] = self.second_form_class(self.request.POST)
        # context['form'] = self.form_class(self.request.POST)
        # response = super().form_invalid(form)
        return self.render_to_response(context)
        # response = super().form_invalid(self.second_form_class)
        # self.second_form_class
        # return response

    def form_valid(self, form):
        try:
            if self.request.method == "POST":
                profile_form = ProfileForm(data=self.request.POST)
                user_form = SignUpForm(data=self.request.POST)
                if user_form.is_valid() and profile_form.is_valid():

                    new_user = user_form.save(commit=False)
                    profile = profile_form.save(commit=False)
                    new_user.set_password(user_form.cleaned_data["password1"])
                    new_user.save()

                    profile.created_by = self.request.user
                    profile.user = new_user
                    profile.save()

                    group = Group.objects.get(name=profile.get_designation_display())
                    group.user_set.add(new_user)
                    return redirect("/employeelist/")
                else:
                    user_form = SignUpForm()
                    profile_form = ProfileForm()
                    messages.error(self.request, "Fields Fill Correctly")
                    return render(
                        self.request,
                        "registration/signup.html",
                        {"form": user_form, "form2": profile_form},
                    )
            else:
                user_form = SignUpForm()
                profile_form = ProfileForm()
                return render(
                    self.request,
                    "registration/signup.html",
                    {"form": user_form, "form2": profile_form},
                )

        except Exception as e:
            # messages.error(self.request,'File Upload Failed')
            # form = EmployeeRegistrationForm(self.request.POST)
            user_form = SignUpForm()
            profile_form = ProfileForm()
            return render(
                self.request,
                "registration/signup.html",
                {"form": user_form, "form2": profile_form},
            )


class EmployeeProfile(DetailView):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.request.user.id)
        if user.user_leaves.all().exists():
            try:
                alloted_leave = user.user_leaves.get(
                    user=request.user, year=datetime.now().year
                )

                get_taken_leave = MonthlyTakeLeave.objects.filter(
                    user=user,
                    year=datetime.now().year,
                    month=datetime.now().month,
                    status=1,
                ).aggregate(Sum("leave"))

                # get_taken_leave_year = MonthlyTakeLeave.objects.filter(user=user,year = datetime.now().year,status=1).aggregate(Sum('leave'))
                get_taken_unpaid_leave = MonthlyTakeLeave.objects.filter(
                    user=user,
                    year=datetime.now().year,
                    month=datetime.now().month,
                    status=2,
                ).aggregate(Sum("leave"))

                available_bonus_leave = (
                    alloted_leave.bonusleave - alloted_leave.available_bonus_leave
                )

                available_leave = (datetime.now().month - alloted_leave.month) + 1

                leave_sum = 0
                if get_taken_leave["leave__sum"]:
                    leave_sum = get_taken_leave["leave__sum"]
                    # available_leave = (datetime.now().month - alloted_leave.month)

                total_available_leave = (
                    available_bonus_leave
                    + available_leave
                    - (leave_sum - alloted_leave.available_bonus_leave)
                )
                # if total_available_leave <= 0:
                #     total_available_leave = 0
                remaning_leave = total_available_leave
                return render(
                    request,
                    "profile.html",
                    {
                        "employee": user,
                        "alloted_leave": alloted_leave,
                        "total_available_leave": total_available_leave,
                        "total_yearly": (
                            alloted_leave.leave + alloted_leave.bonusleave
                        ),
                        "get_taken_leave": get_taken_leave,
                        "get_taken_unpaid_leave": get_taken_unpaid_leave,
                    },
                )

            except AllottedLeave.DoesNotExist:
                return render(request, "profile.html", {"employee": user})
        else:
            return render(request, "profile.html", {"employee": user})


class EmployeeListView(PermissionRequiredMixin, ListView):
    permission_required = ("employee.can_view_user_profile_list",)
    raise_exception = True
    model = Profile
    template_name = "employee_list.html"
    ordering = ["-id"]

    def get_context_data(self, **kwargs):
        context = super(EmployeeListView, self).get_context_data(**kwargs)
        context["active_users"] = context["object_list"].filter(user__is_active=True)
        return context


class AllEmployeeProfile(PermissionRequiredMixin, DetailView):
    permission_required = ("employee.can_view_user_profile_list",)
    raise_exception = True
    # def get(self, request, *args, **kwargs):
    #     user = User.objects.get(pk = kwargs['pk'])
    #     return render(request,'employee_profile.html',{'employee' : user})

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs["pk"])
        if user.user_leaves.all().exists():
            try:
                user = User.objects.get(pk=kwargs["pk"])
                alloted_leave = user.user_leaves.get(
                    user=user, year=datetime.now().year
                )
                get_taken_leave = MonthlyTakeLeave.objects.filter(
                    user=user,
                    year=datetime.now().year,
                    month=datetime.now().month,
                    status=1,
                ).aggregate(Sum("leave"))
                get_taken_unpaid_leave = MonthlyTakeLeave.objects.filter(
                    user=user,
                    year=datetime.now().year,
                    month=datetime.now().month,
                    status=2,
                ).aggregate(Sum("leave"))

                leave_list = Leave.objects.filter(user=user)

                available_bonus_leave = (
                    alloted_leave.bonusleave - alloted_leave.available_bonus_leave
                )
                available_leave = (datetime.now().month - alloted_leave.month) + 1
                leave_sum = 0
                if get_taken_leave["leave__sum"]:
                    leave_sum = get_taken_leave["leave__sum"]
                total_available_leave = (
                    available_bonus_leave
                    + available_leave
                    - (leave_sum - alloted_leave.available_bonus_leave)
                )

                remaning_leave = total_available_leave
                return render(
                    request,
                    "employee_profile.html",
                    {
                        "employee": user,
                        "alloted_leave": alloted_leave,
                        "total_available_leave": total_available_leave,
                        "total_yearly": (
                            alloted_leave.leave + alloted_leave.bonusleave
                        ),
                        "get_taken_leave": get_taken_leave,
                        "get_taken_unpaid_leave": get_taken_unpaid_leave,
                        "leave_list": leave_list,
                    },
                )
            except AllottedLeave.DoesNotExist:
                return render(request, "employee_profile.html", {"employee": user})
        else:
            return render(request, "employee_profile.html", {"employee": user})


class LeaveCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ("employee.add_allottedleave",)
    raise_exception = True
    model = AllottedLeave
    form_class = AllottedLeavesForm
    template_name = "leave.html"
    success_url = "/leaves/"

    def get_context_data(self, **kwargs):
        return dict(
            super(LeaveCreateView, self).get_context_data(**kwargs),
            leave_list=AllottedLeave.objects.all().order_by("-created_at"),
        )

    # def form_valid(self,form):
    #     try:
    #         leave = form.save()
    #         month = self.request.POST.get('month')
    #         monthlyremainingLeave = MonthlyRemainingLeave.objects.create(allotted_leave=leave,month=month,alloted_leave=(leave.bonusleave+1.0))
    #         return HttpResponseRedirect("/leaves/")
    #     except Exception as e:
    #         raise e


class EditAllotedLeaveView(PermissionRequiredMixin, UpdateView):
    permission_required = ("employee.change_allottedleave",)
    raise_exception = True
    model = AllottedLeave
    form_class = AllottedLeavesForm
    template_name = "update_leave.html"
    success_url = "/leaves/"


class EditProfileView(PermissionRequiredMixin, UpdateView):
    permission_required = ("employee.change_profile",)
    raise_exception = True
    model = Profile
    form_class = ProfileForm
    template_name = "update.html"
    success_url = "/employeelist/"

    def post(self, request, *args, **kwargs):
        try:
            instance = Profile.objects.get(pk=kwargs["pk"])
            form = self.form_class(data=request.POST, instance=instance)
            if form.is_valid():
                userdata = form.save()
                userdata.user.first_name = form.data["first_name"]
                userdata.user.last_name = form.data["last_name"]
                userdata.user.email = form.data["email"]
                userdata.user.save()
                return HttpResponseRedirect("/employeelist/")
            else:
                return render(request, "update.html", {"form": form})
        except Exception as e:
            raise


@csrf_exempt
def delete_record(request):
    try:
        for pk in request.POST.getlist("pk[]"):
            obj = EmployeeAttendance.objects.get(pk=pk)
            obj.delete()
        return JsonResponse({"status": "success"})
    except Exception as e:
        print("Uh Oh!, we met some error:", str(e))
        return JsonResponse({"status": "false"})


@csrf_exempt
def deactivate_user(request, pk):
    # import pdb;pdb.set_trace()
    profile = Profile.objects.get(id=pk)
    if request.method == "POST":
        profile.user.is_active = request.POST.get("is_active")
        profile.user.save()
    return JsonResponse({"status": "success"})


@permission_required("employee.add_employeeattendance", raise_exception=True)
def file_upload(request):
    try:
        template = "file_upload.html"
        prompt = {
            "order": "order of csv should be employee_no, in_time, out_time, date"
        }
        if request.method == "GET":
            return render(request, template, prompt)

        excel_file = request.FILES["excel_file"]
        filename = fs.save(excel_file.name, excel_file)
        file_url = settings.PROJECT_APPS + fs.url(
            filename
        )  # project app url + filename
        wb = xlrd.open_workbook(file_url)
        sheet = wb.sheet_by_index(0)

        for i in range(sheet.nrows - 3):
            if i == sheet.nrows - 1:  # row-1
                break
            name = sheet.cell_value(i + 3, 1)
            employee_id = sheet.cell_value(i + 3, 0)
            in_time = sheet.cell_value(i + 3, 3)
            out_time = sheet.cell_value(
                i + 3, sheet.ncols - 1
            )  # sheet.cell_value(i+4,3)
            date = sheet.cell_value(0, 7).split("/")

            if in_time == "--:--" and out_time == "--:--":
                in_time = datetime.strptime("00:00", "%H:%M")
                out_time = datetime.strptime("00:00", "%H:%M")
            elif out_time == "--:--":
                in_time = datetime.strptime(in_time, "%H:%M")
                # out_time = datetime.strptime(in_time ,'%H:%M')
                out_time = in_time
            else:
                in_time = datetime.strptime(in_time, "%H:%M")
                out_time = datetime.strptime(out_time, "%H:%M")

            profile = Profile.objects.filter(employee_id=employee_id)
            if profile.exists():
                profile = Profile.objects.get(employee_id=employee_id)
                emp, created = EmployeeAttendance.objects.update_or_create(
                    user=profile.user,
                    employee_id=profile.employee_id,
                    date=date[2] + "-" + date[1] + "-" + date[0],
                    created_by=profile.user,
                )
                if emp:
                    emp_details = EmployeeAttendanceDetail.objects.filter(
                        employee_attendance=emp
                    )
                    if emp_details.exists():
                        emp_details.delete()
                    detail, created = EmployeeAttendanceDetail.objects.update_or_create(
                        employee_attendance=emp,
                        in_time=in_time,
                        out_time=out_time,
                        date=date[2] + "-" + date[1] + "-" + date[0],
                    )
        messages.success(request, " File Successfully Uploaded.")
        return render(request, template)
    except Exception as e:
        messages.error(request, "File Upload Failed")
        return render(request, template)


def home(request):

    attendances_data = EmployeeAttendance.objects.filter(user=request.user).order_by(
        "-created_at"
    )
    names = set()
    object_list = []
    result = []

    for att in attendances_data:
        if not att.date in names and att.date_time_diffrence() != timedelta(hours=0):
            names.add(att.date)
            result.append(att)

    currunt_month = only_datetime.datetime.now().month
    last_month = currunt_month - 1 if currunt_month > 1 else 12

    for login_hour in result:
        if login_hour.date.month == last_month:
            object_list.append(login_hour)
        elif login_hour.date.month == currunt_month:
            object_list.append(login_hour)
        else:
            pass

    return render(request, "home.html", {"attendances_data": object_list})


def date_time_attendence_view(request):
    attendance = EmployeeAttendance.objects.get(id=request.POST.get("attendance_id"))
    template_name = "partial/date_time_popup.html"
    return render(request, template_name, {"employee_attendence": attendance})


@permission_required("employee.can_view_employee_attendance_list", raise_exception=True)
def employee_details(request, id):
    attendances_data = EmployeeAttendance.objects.filter(user_id=id)
    names = set()
    result = []
    for att in attendances_data:
        if not att.date in names and att.date_time_diffrence() != timedelta(hours=0):
            names.add(att.date)
            result.append(att)

    return render(request, "home.html", {"attendances_data": result})


def show_hour_calender(request):
    attendances_data = EmployeeAttendance.objects.filter(user=request.user.id)
    # leaves = Leave.objects.filter(user=request.user)
    # urgent_leave = []
    # for leave in leaves:
    #     urgent_leave.append(Leave.objects.filter(startdate = leave.startdate,enddate = leave.enddate, user=request.user, select_leave = 2))
    # count=0
    # names = set()
    # result = []
    # for att in attendances_data:
    #     if not att.date in names:
    #         names.add(att.date)
    #         result.append(att)
    # for leave in select_leaves:
    #     if leave.select_leave == 2:
    #             count+=1
    # urgrnt_leave = count

    return render(request, "fullcalendar.html", {"attendances_data": attendances_data})


def show_calendar(request, id):
    attendances_data = EmployeeAttendance.objects.filter(user_id=id)
    names = set()
    result = []
    for att in attendances_data:
        if not att.date in names:
            names.add(att.date)
            result.append(att)

    return render(request, "fullcalendar.html", {"attendances_data": result})


# @csrf_exempt
# def request_leave(request):

#     import datetime
#     if request.method == 'POST':
#         date_list = request.POST.getlist('leaveRequestArr[]')
#         attendance_request_list = EmployeeAttendance.objects.filter(date__in=date_list ,user=request.user)
#         for attendance in attendance_request_list:
#             attendance.empatt_leave_status = 2
#             attendance.save()
#             frm = 'ankita@thoughtwin.com'
#             text_content = request.user.username+ ',Leave request send for less hours'
#             email = EmailMessage("Leave request for less hours",text_content,frm,to=["ankita@thoughtwin.com"])

#             email.send()
#         return JsonResponse({'status': 'success'})


class LeaveRequestView(View):
    model = EmployeeAttendance

    def post(self, request):
        import datetime

        try:
            if request.method == "POST":
                date_list = request.POST.getlist("leaveRequestArr[]")
                time_list = request.POST.getlist("loginHour[]")
                attendance_request_list = EmployeeAttendance.objects.filter(
                    date__in=date_list, user=request.user
                )
                for attendance in attendance_request_list:
                    # emails = request.POST.getlist('emails[]')
                    attendance.empatt_leave_status = 2
                    attendance.save()

                mail_list = []
                default_mail_list = User.objects.filter(groups__name__in=["MD", "HR"])
                for usr in default_mail_list:
                    mail_list.append(usr.email)
                request_user = request.user.email
                mail_list.append(request_user)
                mail_list.append(request.user.profile.teamlead.email)
                mail_list = set(mail_list)

                request_send_list = []

                request_list = User.objects.filter(groups__name__in=["MD", "HR"])
                for usr in request_list:
                    # emails.append(usr.email)

                    request_send_list.append(usr.first_name + " " + usr.last_name)
                request_send_list.append(
                    self.request.user.profile.teamlead.first_name
                    + " "
                    + self.request.user.profile.teamlead.last_name
                )
                request_send_list = set(request_send_list)

                # full_name = []
                # full_name.append(self.request.user.first_name)
                # full_name.append(self.request.user.last_name)
                # user = full_name[0] +" "+ full_name[1]
                full_name = (
                    self.request.user.first_name + " " + self.request.user.last_name
                )
                user = full_name.title()

                user_date_list = []

                for date_lists in date_list:
                    date_email = date_lists.split("-")
                    send_email_data = date(
                        int(date_email[0]), int(date_email[1]), int(date_email[2])
                    )
                    user_date_list.append(send_email_data.strftime("%b %d, %Y"))

                subject_date = attendance.date.strftime("%b %d, %Y")
                content = render_to_string(
                    "email/less_leave_mail_content.html",
                    {
                        "email_user": user,
                        "date_list": user_date_list,
                        "request_send_list": request_send_list,
                        "date_time_diffrence": time_list,
                    },
                )

                email_subject = (
                    "Leave Request For Less Hour ||"
                    " " + user + " "
                    "||"
                    " " + subject_date
                )

                text_content = strip_tags(content)

                for email in mail_list:
                    msg = EmailMultiAlternatives(
                        email_subject, text_content, settings.FROM_EMAIL, [email]
                    )
                    msg.attach_alternative(content, "text/html")
                    msg.send()
                return JsonResponse({"status": "success"})

        except Exception as e:
            print(str(e))
            # text_content = request.user.username+ ',Leave request send for less hours'
            # email = EmailMessage("Leave request for less hours",text_content,settings.FROM_EMAIL,to=mail_list)
            # email.send()
            return JsonResponse({"status": "error"})


class LeaveListView(PermissionRequiredMixin, ListView):
    permission_required = ("employee.can_view_employee_attendance_list",)
    raise_exception = True
    model = EmployeeAttendance
    template_name = "leave_list.html"

    def get_context_data(self, **kwargs):
        context = super(LeaveListView, self).get_context_data(**kwargs)
        context["object_list"] = self.model.objects.filter(
            empatt_leave_status__in=[2, 3, 4]
        )
        return context


def attendence_request_list(request):

    attendances = (
        EmployeeAttendance.objects.filter(
            user=request.user, empatt_leave_status__in=[1, 3, 4, 5, 6]
        )
        .exclude(employee_attendance__in_time="00:00:00")
        .order_by("-created_at")
    )
    result = []
    email_data = []
    # and attendance.date_time_diffrence() != timedelta(hours=0)
    for attendance in attendances:

        if attendance.user.profile.working_time == 7 and attendance.date_time_diffrence() < timedelta(
            hours=9
        ):

            result.append(attendance)
        elif attendance.user.profile.working_time == 5 and attendance.date_time_diffrence() < timedelta(
            hours=8
        ):

            result.append(attendance)
        elif attendance.user.profile.working_time == 3 and attendance.date_time_diffrence() < timedelta(
            hours=7
        ):

            result.append(attendance)
        elif attendance.user.profile.working_time == 1 and attendance.date_time_diffrence() < timedelta(
            hours=6
        ):

            result.append(attendance)
        elif attendance.user.profile.working_time == 6 and attendance.date_time_diffrence() < timedelta(
            hours=8, minutes=30
        ):

            result.append(attendance)
        elif attendance.user.profile.working_time == 4 and attendance.date_time_diffrence() < timedelta(
            hours=7, minutes=30
        ):

            result.append(attendance)
        elif attendance.user.profile.working_time == 2 and attendance.date_time_diffrence() < timedelta(
            hours=6, minutes=30
        ):

            result.append(attendance)

    object_list = []

    currunt_month = only_datetime.datetime.now().month
    last_month = currunt_month - 1 if currunt_month > 1 else 12
    for less_hour in result:
        if less_hour.date.month == last_month:
            object_list.append(less_hour)
        elif less_hour.date.month == currunt_month:
            object_list.append(less_hour)
        else:
            pass
    # context['object_list'] = object_list

    mail_list = []
    default_mail_list = User.objects.filter(groups__name__in=["MD", "HR"])
    for usr in default_mail_list:
        mail_list.append(usr.email)
    request_user = request.user.email
    mail_list.append(request_user)
    mail_list.append(request.user.profile.teamlead.email)
    mail_list = set(mail_list)
    # aaccept_email_data = []
    # default_mail_list = User.objects.filter(groups__name__in=['MD','HR'])
    # for usr in default_mail_list:
    #         aaccept_email_data.append(usr.email)

    # for user in User.objects.all():
    #         email_data.append(user.email)
    #         email_data.sort()
    # return render(request,'red_list.html', {'attendance_data' : result,'emails':mail_list,'aaccept_email_data':aaccept_email_data})
    return render(
        request,
        "red_list.html",
        {"attendance_data": object_list, "mail_list": mail_list},
    )


# def leave_status(request): # reject/accept leave hour
#     email_data = []
#     leave_id = request.POST.get("leave_id")
#     employee_attendance = EmployeeAttendance.objects.get(id=leave_id)
#     employee_attendance. empatt_leave_status = request.POST.get("leave_type")
#     employee_attendance.save()
#     message = "dummy"
#     if employee_attendance. empatt_leave_status == '3':
#         message = employee_attendance.user.username +",Leave accept by "+request.user.username+" for less hour"
#     if employee_attendance. empatt_leave_status == '4':
#         message = employee_attendance.user.username +",Leave reject by "+request.user.username+" for less hour"

#     frm = 'ankita@thoughtwin.com'
#     email = EmailMessage("Leave response for less hour",message,frm,to=["ankita@thoughtwin.com"])
#     email.send()

#     return JsonResponse({'status': 'success'})


class LeaveStatusView(View):

    model = EmployeeAttendance

    def post(self, request):
        try:
            leave_id = request.POST.getlist("leave_id[]")
            # date_list = request.POST.getlist('leaveRequestArr[]')
            # time_list = request.POST.getlist('loginHour[]')
            # leave_user = request.POST.get('leave_user')
            less_hour_date = []
            user_data = []

            for employee_id in leave_id:
                employee_attendance = EmployeeAttendance.objects.get(id=employee_id)
                less_hour_date = employee_attendance.date.strftime("%b %d, %Y")
                time_diff = employee_attendance.date_time_diffrence()

                employee_attendance.empatt_leave_status = "3"
                employee_attendance.save()
                # email_date = employee_attendance.date.strftime("%b %d, %Y")
                full_name = (
                    employee_attendance.user.first_name
                    + " "
                    + employee_attendance.user.last_name
                )
                user = full_name.title()
                approved_full_name = (
                    self.request.user.first_name + " " + self.request.user.last_name
                )
                approved_user = approved_full_name.title()

                user_data.append(
                    {
                        "emp": employee_attendance.user.email,
                        "emp_tl": employee_attendance.user.profile.teamlead.email,
                        "emp_date": less_hour_date,
                        "login_time": time_diff,
                        "name": user,
                        "approved_user": approved_user,
                    }
                )

            dt_list = []
            tm_list = []

            for user in user_data:
                emp = user
                dt_list.append(emp["emp_date"])
                tm_list.append(emp["login_time"])
            data = user_data[0]
            data.pop("emp_date")
            data.pop("login_time")
            data["emp_date"] = dt_list
            data["login_time"] = tm_list

            mail_list = []
            default_mail_list = User.objects.filter(groups__name__in=["MD", "HR"])
            for usr in default_mail_list:
                mail_list.append(usr.email)

            mail_list.append(data["emp"])
            mail_list.append(data["emp_tl"])

            # -----------email subject
            email_subject = "Leave Approved For Less Hour ||" " " + data["name"]
            #     # email_subject = "Leave Approved For Less Hour ||"" "+emp_tl_email['name']+" "'||'" "+emp_tl_email['emp_date'][0]

            # -----------email content
            content = render_to_string(
                "email/approved_less_leave.html",
                {
                    "approved_user": data["approved_user"],
                    "user": data["name"],
                    "date_lists": data["emp_date"],
                    "date_time_diffrence": data["login_time"],
                },
            )
            text_content = strip_tags(content)

            msg = EmailMultiAlternatives(
                email_subject, text_content, settings.FROM_EMAIL, mail_list
            )

            msg.attach_alternative(content, "text/html")
            msg.send()
            return JsonResponse({"status": "success"})
        except Exception as e:
            print(str(e))
            return JsonResponse({"status": "error"})


@csrf_exempt
def delete_record(request):
    if request.method == "POST":
        data = request.POST.getlist("data[]")
        empatt = EmployeeAttendance.objects.filter(id__in=data)
        empatt.delete()
        return JsonResponse({"status": "success"})


# class RequestLeaveView(PermissionRequiredMixin,CreateView):
class RequestLeaveView(CreateView):
    # permission_required = ('quotes.add_quote', )
    # raise_exception = True
    model = Leave
    form_class = LeaveCreateForm
    template_name = "request_leave.html"
    success_url = "/leave/"

    def form_valid(self, form, **kwargs):
        try:
            form = self.form_class(data=form.data)
            leave = form.save(commit=False)
            leave_date = form.data["startdate"].split("-")
            year = int(leave_date[0])
            try:
                next_year = date.today().year + 1
                if year == next_year:
                    messages.error(
                        self.request,
                        "You Have Not Allotted Any Leave of this year please contact to HR",
                    )
                    return HttpResponseRedirect("/leave")
                alloated_leave = AllottedLeave.objects.get(
                    user=self.request.user, year=datetime.now().year
                )
            except ObjectDoesNotExist:
                messages.error(self.request, "You Have Not Allotted Any Leave")
                return HttpResponseRedirect("/leave")

            # leave_year =  alloated_leave.year
            # if year == datetime.datetime.now().year:
            if "starttime" in form.data:
                starttime = form.data["starttime"]
                starttime = datetime.strptime(starttime, "%H:%M")

                # endtime = form.data['endtime']
                # endtime = datetime.strptime(endtime ,'%H:%M')
                endtime = starttime + timedelta(hours=4)
                # if starttime >= endtime:
                #     messages.error(self.request, 'End Time Not Valid')
                #     email_data = []
                #     email = email_data
                #     for user in User.objects.all():
                #         email_data.append(user.email)
                #         email_data.sort()
                #     return render(self.request,'request_leave.html',{'form':form ,'emails':email})

                # starttime = starttime.strftime('%I:%M %p')
                # endtime = endtime.strftime('%I:%M %p')

                leave.starttime = starttime  # form.data['starttime']
                leave.endtime = endtime  # form.data['starttime']
            startdate1 = form.data["startdate"]
            startdate = form.data["startdate"].split("-")
            enddate = form.data["enddate"].split("-")
            d1 = date(
                int(startdate[0]), int(startdate[1]), int(startdate[2])
            )  # startdate
            d2 = date(int(enddate[0]), int(enddate[1]), int(enddate[2]))  # startdate
            delta = d2 - d1
            leave_type = form.data["leave_type"]
            for i in range(delta.days + 1):
                if leave_type == "2":
                    # delete existing obj if file uploaded before leave request only in halfday case.
                    leave_obj = EmployeeAttendance.objects.filter(
                        user=self.request.profile.user,
                        employee_id=self.request.profile.employee_id,
                        date=startdate1,
                    )
                    leave_obj.delete()

                    emp, created = EmployeeAttendance.objects.update_or_create(
                        user=self.request.profile.user,
                        employee_id=self.request.profile.employee_id,
                        date=d1 + timedelta(days=i),
                        created_by=self.request.user,
                        empatt_leave_status=5,
                        leave_day_time="0.5",
                    )

                if leave_type == "3":
                    emp, created = EmployeeAttendance.objects.update_or_create(
                        user=self.request.profile.user,
                        employee_id=self.request.profile.employee_id,
                        date=d1 + timedelta(days=i),
                        created_by=self.request.user,
                        empatt_leave_status=5,
                        leave_day_time="1.0",
                    )

            leave.leave_type = form.data["leave_type"]
            leave.select_leave = form.data["select_leave"]
            leave.user = self.request.user
            if Leave.objects.filter(
                startdate=startdate1, user=self.request.profile.user
            ).exists():
                messages.error(self.request, "Already sent request")
                return HttpResponseRedirect("/leave")
            else:
                leave.save()
            leaveDetail = LeaveDetails.objects.create(
                leave=leave, reason=form.data["reason"], created_by=self.request.user
            )

            # for MD , HR and teamlead
            mail_list = []
            default_mail_list = User.objects.filter(groups__name__in=["MD", "HR"])
            for usr in default_mail_list:
                # emails.append(usr.email)
                mail_list.append(usr.email)
            request_user = self.request.user.email
            mail_list.append(request_user)
            mail_list.append(self.request.user.profile.teamlead.email)

            emails = self.request.POST.get("emails").split(",")
            for email in emails:
                mail_list.append(email)
            mail_list = set(mail_list)

            request_send_list = []

            request_list = User.objects.filter(groups__name__in=["MD", "HR"])
            for usr in request_list:
                # emails.append(usr.email)
                request_send_list.append(usr.first_name + " " + usr.last_name)
            request_send_list.append(
                self.request.user.profile.teamlead.first_name
                + " "
                + self.request.user.profile.teamlead.last_name
            )
            request_send_list = set(request_send_list)

            full_name = self.request.user.first_name + " " + self.request.user.last_name
            user = full_name.title()

            if leave_type == "2":
                content = render_to_string(
                    "email/email_content.html",
                    {
                        "email_user": user,
                        "startdate": d1,
                        "reason": form.data["reason"],
                        "request_send_list": request_send_list,
                    },
                )
            if leave_type == "3":
                content = render_to_string(
                    "email/email_content.html",
                    {
                        "email_user": user,
                        "startdate": d1,
                        "enddate": d2,
                        "reason": form.data["reason"],
                        "request_send_list": request_send_list,
                    },
                )
            start_date = d1
            end_date = d2
            email_startdate = start_date.strftime("%b %d, %Y")
            email_enddate = end_date.strftime("%b %d, %Y")
            text_content = strip_tags(content)
            if form.data["leave_type"] == "2":
                email_subject = (
                    "Leave Request ||"
                    " " + user + " "
                    "||"
                    " " + "Half Day" + " "
                    "||"
                    " " + str(email_startdate)
                )
            if form.data["leave_type"] == "3":
                email_subject = (
                    "Leave Request ||"
                    " " + user + " "
                    "||"
                    " " + "Full Day"
                    " " + "||"
                    " " + str(email_startdate) + "-" + str(email_enddate)
                )
            for email in mail_list:
                try:
                    msg = EmailMultiAlternatives(
                        email_subject, text_content, settings.FROM_EMAIL, [email]
                    )
                    msg.attach_alternative(content, "text/html")
                    msg.send()
                except Exception as e:
                    pass
            messages.success(self.request, "Leave Request Sent Successfully")

            # 'mail_list':mail_list - get mail list
            # return render(self.request,'request_leave.html', {'accept_emails' : mail_lists})
            return HttpResponseRedirect("/leave")
            # else:
            #     messages.error(self.request, 'Leave Are Not Alloted In This Year')
            #     return HttpResponseRedirect('/leave')
        except IntegrityError:
            messages.error(self.request, "Leave Request Already Send")
            return HttpResponseRedirect("/leave")

    def get_context_data(self, **kwargs):
        context = super(RequestLeaveView, self).get_context_data(**kwargs)
        context["object_list"] = self.model.objects.all()
        # default_mail_list = User.objects.filter(groups__name__in=['MD','HR'])

        # for usr in default_mail_list:
        #     mail_list.append(usr.email)
        # context['emails'] = email_data

        mail_list = []
        default_mail_list = User.objects.filter(groups__name__in=["MD", "HR"])
        for usr in default_mail_list:
            mail_list.append(usr.email)
        request_user = self.request.user.email
        mail_list.append(request_user)
        mail_list.append(self.request.user.profile.teamlead.email)

        email_data = []
        groups_email = []

        for user in User.objects.all():
            if user.email in mail_list:
                groups_email.append(user.email)
            else:
                email_data.append(user.email)
                email_data.sort()

        email_data = set(email_data)
        mail_list = set(mail_list)

        context["mail_list"] = mail_list
        context["email_data"] = email_data

        return context


# this function show all leave list to HR or MD
class AllEmpLeaveListView(ListView):
    # class EmpLeaveListView(PermissionRequiredMixin,ListView):
    # permission_required = ('employee.can_view_leave_list',)
    # raise_exception = True
    model = Leave
    queryset = Leave.objects.all()
    template_name = "leave/all_leave_list.html"
    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):
        context = super(AllEmpLeaveListView, self).get_context_data(**kwargs)
        # context['object_list'] = Leave.objects.filter(status=1)
        if self.request.user.groups.exists():
            group_name = self.request.user.groups.first().name
            currunt_date = only_datetime.datetime.now()
            cr_year = only_datetime.datetime.now().year
            cr_month = only_datetime.datetime.now().month
            cr_eleventh_day = only_datetime.datetime(
                year=cr_year, month=cr_month, day=11
            )
            cr_first_day = only_datetime.datetime(year=cr_year, month=cr_month, day=1)
            nextmonth_eleventh_day = date.today() + relativedelta.relativedelta(
                months=1, day=11
            )
            lastmonth_first_day = date.today() - relativedelta.relativedelta(
                months=1, day=1
            )

            if currunt_date < cr_eleventh_day:
                context["object_list"] = self.queryset.filter(
                    status__in=[1, 2, 3],
                    created_at__range=(lastmonth_first_day, cr_eleventh_day),
                )
            else:
                context["object_list"] = self.queryset.filter(
                    status__in=[1, 2, 3],
                    created_at__range=(cr_first_day, nextmonth_eleventh_day),
                )
            return context
            # last_month = currunt_month-1 if currunt_month > 1 else 12
            # last_year = now.year - 1
            # currunt_date = str(currunt_month).split(' ')

        # usr = User.objects.filter(email=self.request.user.email)
        # profiles = Profile.objects.filter(teamlead=usr[0])
        # users =[]
        # for profile in profiles:
        #     users.append(profile.user)
        # context['object_list'] = self.model.objects.filter(user__in=users)
        # return context


class EmpLeaveListView(ListView):
    model = Leave
    template_name = "leave/leave_list.html"
    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):
        context = super(EmpLeaveListView, self).get_context_data(**kwargs)

        usr = User.objects.filter(email=self.request.user.email)
        profiles = Profile.objects.filter(teamlead=usr[0])
        users = []
        for profile in profiles:
            users.append(profile.user)
        context["object_list"] = self.model.objects.filter(user__in=users)
        return context


class MyLiveListView(ListView):
    model = Leave
    queryset = Leave.objects.all()
    template_name = "leave/my_leave_list.html"

    def get_context_data(self, **kwargs):
        context = super(MyLiveListView, self).get_context_data(**kwargs)
        usr = self.request.user.id
        context["object_list"] = self.queryset.filter(user=usr)
        select_leaves = self.queryset.filter(user=usr)
        return context


def full_leave(request):
    try:
        if request.method == "POST":
            dateleave = []
            user = request.user
            emp_id = request.user.id
            start = request.POST.get("start_date")
            end = request.POST.get("end_date")
            emp_type = request.POST.get("emp_type")
            start_date = parse_date(start)
            end_date = parse_date(end)
            delta = end_date - start_date
            for i in range(delta.days + 1):
                date = start_date + timedelta(days=i)
                EmployeeAttendance.objects.update_or_create(
                    user=user,
                    employee_id=emp_id,
                    date=date,
                    empatt_leave_status=emp_type,
                )
        return JsonResponse({"status": "success"})
    except Exception as e:
        messages.error(request, "Already Exist")
        return render(request, "fullday_leave_list.html",)


def full_leave_status(request):
    if request.method == "POST":
        leave_id = request.POST.get("leave_id")
        # leave_user =request.POST.get("leave_user")
        leave_type = request.POST.get("leave_type")
        leave_status = request.POST.get("leave_status")
        leave = Leave.objects.get(id=leave_id)
        leave_status = False
        if leave.status == 2:
            leave_status = True
        leave.status = request.POST.get("leave_status")
        leave.save()

        leavedetails = LeaveDetails.objects.filter(leave=leave)
        for leavedetail in leavedetails:
            if leave_status:
                leavedetail.status = request.POST.get("leave_status")
                leavedetail.save()
            else:
                LeaveDetails.objects.create(
                    leave=leave,
                    status=request.POST.get("leave_status"),
                    reason=leavedetail.reason,
                    created_by=request.user,
                )
        startdate = leave.startdate
        enddate = leave.enddate
        delta = enddate - startdate
        count = 0
        for day in range(delta.days + 1):
            count += 1
            employee_attendence = EmployeeAttendance.objects.filter(
                user=leave.user, date=startdate + timedelta(days=day)
            )
            names = set()
            result = []
            for att in employee_attendence:
                if not att.date in names:
                    names.add(att.date)
                    result.append(att)
            for employee_attendence in result:
                if leave.status == "2":
                    employee_attendence.empatt_leave_status = 6
                if leave.status == "3":
                    employee_attendence.empatt_leave_status = 7
                employee_attendence.save()

        if leave_type == "Half day":
            count = 0.5
        # when leave reject deduct leave from employee account.
        if int(leave.status) == 3:
            if leave_status:
                get_taken_leave_unpaid = MonthlyTakeLeave.objects.filter(
                    user=leave.user,
                    year=leave.startdate.year,
                    month=leave.startdate.month,
                    status=2,
                    leave=count,
                ).first()
                if get_taken_leave_unpaid == None:
                    get_taken_leave_paid = MonthlyTakeLeave.objects.filter(
                        user=leave.user,
                        year=leave.startdate.year,
                        month=leave.startdate.month,
                        status=1,
                        leave=count,
                    ).first()
                    if get_taken_leave_paid == None:
                        get_taken_leave = MonthlyTakeLeave.objects.filter(
                            user=leave.user,
                            year=leave.startdate.year,
                            month=leave.startdate.month,
                            status__in=[1, 2],
                        ).order_by("-id")[:2]
                        for item in get_taken_leave:
                            item.delete()
                    else:
                        get_taken_leave_paid.delete()
                else:
                    get_taken_leave_unpaid.delete()

        if int(leave.status) == 2:

            alloted_leave = leave.user.user_leaves.filter(
                year=leave.startdate.year
            ).first()
            get_taken_leave = MonthlyTakeLeave.objects.filter(
                user=leave.user,
                year=leave.startdate.year,
                month=leave.startdate.month,
                status=1,
            ).aggregate(Sum("leave"))
            gettaken = 0
            if get_taken_leave["leave__sum"]:
                gettaken = get_taken_leave["leave__sum"]

            available_bonus_leave = (
                alloted_leave.bonusleave - alloted_leave.available_bonus_leave
            )
            available_leave = (leave.startdate.month - alloted_leave.month) + 1

            total_available_leave = (
                available_bonus_leave
                + available_leave
                - (gettaken - alloted_leave.available_bonus_leave)
            )

            if total_available_leave >= count:
                monthly_take_leave = MonthlyTakeLeave.objects.create(
                    user=leave.user,
                    year=leave.startdate.year,
                    month=leave.startdate.month,
                    status=1,
                    leave=count,
                )

                if available_bonus_leave > 0:
                    if available_bonus_leave >= count:
                        alloted_available_bonus_leave = (
                            alloted_leave.available_bonus_leave + count
                        )
                    else:
                        alloted_available_bonus_leave = (
                            alloted_leave.available_bonus_leave + available_bonus_leave
                        )

                    alloted_leave.available_bonus_leave = alloted_available_bonus_leave
                    alloted_leave.save()
                    # remaining_count = count-available_bonus_leave
                # else:
            else:
                if available_bonus_leave > 0:
                    if available_bonus_leave >= count:
                        alloted_available_bonus_leave = (
                            alloted_leave.available_bonus_leave + count
                        )
                    else:
                        alloted_available_bonus_leave = (
                            alloted_leave.available_bonus_leave + available_bonus_leave
                        )
                    alloted_leave.available_bonus_leave = alloted_available_bonus_leave
                    alloted_leave.save()
                    # remaining_count = count-available_bonus_leave

                unpaid_leave = count - total_available_leave
                monthly_take_leave = MonthlyTakeLeave.objects.create(
                    user=leave.user,
                    year=leave.startdate.year,
                    month=leave.startdate.month,
                    status=1,
                    leave=total_available_leave,
                )
                monthly_take_leave = MonthlyTakeLeave.objects.create(
                    user=leave.user,
                    year=leave.startdate.year,
                    month=leave.startdate.month,
                    status=2,
                    leave=unpaid_leave,
                )

        # end monthly model
        # ------------------------------------------------------------

        aaccept_email_data = []
        aaccept_email_data.append(leave.user.profile.teamlead.email)
        aaccept_email_data.append(leave.user.email)
        default_mail_list = User.objects.filter(groups__name__in=["MD", "HR"])
        for usr in default_mail_list:
            aaccept_email_data.append(usr.email)
        data_email = set(aaccept_email_data)

        email_data = []
        for user in User.objects.all():
            email_data.append(user.email)
        full_name = leave.user.first_name + " " + leave.user.last_name
        user = full_name.title()
        approve_fullname = []
        approve_fullname.append(request.user.first_name)
        approve_fullname.append(request.user.last_name)
        approve_user_fullname = approve_fullname[0] + " " + approve_fullname[1]
        startdate = startdate.strftime("%b %d, %Y")
        enddate = enddate.strftime("%b %d, %Y")
        if leave.status == "2":
            if leave_type == "Half day":
                email_subject = (
                    "Leave Approved "
                    "||"
                    " " + user + " "
                    "|| Half Day"
                    " "
                    "||"
                    " " + startdate
                )

                content = render_to_string(
                    "email/accept_leave_request_mail.html",
                    {
                        "user": user,
                        "accept_user": approve_user_fullname,
                        "startdate": startdate,
                        "reason": leavedetail.reason,
                        "daytype": leave_type,
                    },
                )
            if leave_type == "Full day":
                email_subject = (
                    "Leave Approved "
                    "||"
                    " " + user + " "
                    "|| Full Day"
                    " "
                    "||"
                    " " + startdate + "-" + enddate
                )
                content = render_to_string(
                    "email/accept_leave_request_mail.html",
                    {
                        "user": user,
                        "accept_user": approve_user_fullname,
                        "startdate": startdate,
                        "enddate": enddate,
                        "reason": leavedetail.reason,
                        "daytype": leave_type,
                    },
                )
        if leave.status == "3":
            if leave_type == "Half day":
                email_subject = (
                    "Leave Rejected "
                    "||"
                    " " + user + " "
                    "|| Half Day"
                    " "
                    "||"
                    " " + startdate
                )
                content = render_to_string(
                    "email/reject_leave_request_mail.html",
                    {
                        "user": user,
                        "accept_user": approve_user_fullname,
                        "startdate": startdate,
                        "reason": leavedetail.reason,
                        "daytype": leave_type,
                    },
                )
            if leave_type == "Full day":
                email_subject = (
                    "Leave Rejected "
                    "||"
                    " " + user + " "
                    "|| Full Day"
                    " "
                    "||"
                    " " + startdate + "-" + enddate
                )
                content = render_to_string(
                    "email/reject_leave_request_mail.html",
                    {
                        "user": user,
                        "accept_user": approve_user_fullname,
                        "startdate": startdate,
                        "enddate": enddate,
                        "reason": leavedetail.reason,
                        "daytype": leave_type,
                    },
                )

        text_content = strip_tags(content)
        for email in data_email:
            try:
                msg = EmailMultiAlternatives(
                    email_subject, text_content, settings.FROM_EMAIL, [email]
                )
                msg.attach_alternative(content, "text/html")
                msg.send()
            except Exception as e:
                pass
        # accept_email = EmailMessage("Leave Response",message,settings.FROM_EMAIL,to=data_email)
        # accept_email.send()

        # It's only run when leave approve and leave startdate is today date.
        # if leave.status == '2' and leave.is_ooo_send == False:
        #     if leave.startdate == datetime.now().date():
        #         if leave_type == 'Half day':
        #             email_subject = "OOO ||"" "+user+" "'||'" "+leave_type+" "'||'" "+startdate
        #             content = render_to_string('email/ooo_email_content.html',{'user':user,'startdate':startdate,'reason':leavedetail.reason  })
        #         if leave_type == 'Full day':
        #             email_subject = "OOO ||"" "+user+" "'||'" "+leave_type+" "'||'" "+startdate+"-"+enddate
        #             content = render_to_string('email/ooo_email_content.html',{'user':user,'startdate':startdate,'enddate':enddate,'reason':leavedetail.reason  })
        #         # email_data
        #         text_content = strip_tags(content)
        #         for email in email_data:
        #             try:
        #                 msg = EmailMultiAlternatives(email_subject, text_content, settings.FROM_EMAIL,[email])
        #                 msg.attach_alternative(content, "text/html")
        #                 msg.send()
        #                 leave.is_ooo_send = True
        #                 leave.save()
        #             except Exception as e:
        #                 pass

    return JsonResponse({"status": "success"})


# click send_mail button after reject leave.
def send_ooo_on_reject(request):
    if request.method == "POST":
        leave_id = request.POST.get("leave_id")
        leave_user = request.POST.get("leave_user")
        leave_type = request.POST.get("leave_type")
        leave = Leave.objects.get(id=request.POST.get("leave_id"))
        get_leave_obj = Leave.objects.get(id=leave_id)
        startdate = leave.startdate.strftime("%b %d, %Y")
        enddate = leave.enddate.strftime("%b %d, %Y")
        #import pdb; pdb.set_trace();
        leavedetail = LeaveDetails.objects.filter(leave=get_leave_obj)
        for mail in leavedetail:
            if mail.status == 3 and leave.is_ooo_send == False:
                if leave.leave_type == 2:
                    email_subject = (
                        "OOO ||"
                        " " + leave.user.profile.full_name + " "
                        "||"
                        " " + leave.get_leave_type_display() + " "
                        "||"
                        " " + startdate
                    )
                    content = render_to_string(
                        "email/ooo_email_content.html",
                        {
                            "user": leave.user,
                            "startdate": startdate,
                            "reason": mail.reason,
                        },
                    )
                if leave.leave_type == 3:
                    email_subject = (
                        "OOO ||"
                        " " + leave.user.profile.full_name + " "
                        "||"
                        " " + leave.get_leave_type_display() + " "
                        "||"
                        " " + startdate + "-" + enddate
                    )
                    content = render_to_string(
                        "email/ooo_email_content.html",
                        {
                            "user": leave.user,
                            "startdate": startdate,
                            "enddate": enddate,
                            "reason": mail.reason,
                        },
                    )
                # email_data
                text_content = strip_tags(content)
                for user in User.objects.all():
                    try:
                        msg = EmailMultiAlternatives(
                            email_subject,
                            text_content,
                            settings.FROM_EMAIL,
                            [user.email],
                        )
                        msg.attach_alternative(content, "text/html")
                        msg.send()
                        leave.is_ooo_send = True
                        leave.save()
                    except Exception as e:
                        pass
    return JsonResponse({"status": "success"})


class FullLeaveListView(PermissionRequiredMixin, ListView):

    permission_required = ("employee.can_view_employee_attendance_list",)

    raise_exception = True
    model = EmployeeAttendance
    template_name = "fullday_leave_list.html"

    def get_context_data(self, **kwargs):
        context = super(FullLeaveListView, self).get_context_data(**kwargs)
        # context['object_list'] = self.model.objects.filter(empatt_leave_status__in=[2,3,4]).order_by('-created_at')
        object_list = []
        less_time_objects = self.model.objects.filter(
            empatt_leave_status__in=[2,]
        ).order_by("-created_at")
        currunt_month = only_datetime.datetime.now().month
        last_month = currunt_month - 1 if currunt_month > 1 else 12
        for less_hour in less_time_objects:
            if less_hour.date.month == last_month:
                object_list.append(less_hour)
            elif less_hour.date.month == currunt_month:
                object_list.append(less_hour)
            else:
                pass

        context["object_list"] = object_list
        return context


class InOutTimeListView(ListView):
    model = EmployeeAttendance
    template_name = "in_out_time_request.html"

    def get_context_data(self, **kwargs):
        context = super(InOutTimeListView, self).get_context_data(**kwargs)
        usr = User.objects.filter(email=self.request.user.email)
        profiles = Profile.objects.filter(teamlead=usr[0])
        currunt_month = only_datetime.datetime.now().month
        last_month = currunt_month - 1 if currunt_month > 1 else 12
        object_list = []
        # for profile in profiles:
        #     count = 0
        #     less_time_objects = self.model.objects.filter(empatt_leave_status__in=[2,3,4],user=profile.user)
        #     for last_two_user in less_time_objects:
        #         if count >= 2:
        #             break;
        #         elif last_two_user.date.month == last_month or currunt_month:
        #             if last_two_user.empatt_leave_status == 2:
        #                 if count < 2:
        #                     object_list.append(last_two_user)
        #                     count +=1
        #                 else:
        #                     break
        #             elif last_two_user.empatt_leave_status == 3:
        #                 object_list.append(last_two_user)
        #             else:
        #                 pass
        for profile in profiles:
            less_time_objects = self.model.objects.filter(
                empatt_leave_status__in=[2,], user=profile.user
            ).order_by("-id")[:2]
            for login_time in less_time_objects:
                if login_time.date.month == last_month:
                    object_list.append(login_time)
                elif login_time.date.month == currunt_month:
                    object_list.append(login_time)

        context["object_list"] = object_list

        return context


def change_password(request):
    try:
        if request.user.is_authenticated:

            form = changePassForm(request.POST or None)

            old_password = request.POST.get("old_password")
            new_password = request.POST.get("new_password")
            re_new_password = request.POST.get("re_new__password")

            if request.POST.get("old_password"):

                user = User.objects.get(username=request.user.username)
                if user.check_password("{}".format(old_password)) == False:
                    form.set_old_password_flag()

            if form.is_valid():

                user.set_password("{}".format(new_password))
                user.save()
                update_session_auth_hash(request, user)

                return HttpResponseRedirect("/login/")

            else:
                return render(request, "change_password.html", {"form": form})

        else:
            return HttpResponseRedirect("/login/")

    except Exception as e:
        raise


class ForgotPassword(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "home.html")
        else:
            return render(request, "registration/forgot-password.html")

    def post(self, request):
        try:
            if request.method == "POST":
                email = request.POST["email"]
                try:
                    user = User.objects.get(email=email)
                except Exception as e:

                    messages.error(self.request, "Email Not Exist")
                    return HttpResponseRedirect("/forgot-password/")

                password = User.objects.make_random_password(
                    length=8, allowed_chars="123456789"
                )
                user.set_password(password)
                user.save()
                body = (
                    "Hi there. \n You have requested a new password for your account on Testing.\nYour temporary password is "
                    + password
                    + ""
                )
                send_mail = EmailMessage(
                    "Forgot password", body, settings.FROM_EMAIL, to=[user.email]
                )
                send_mail.send()
                messages.success(self.request, "Check Your Password In Mail")
                return HttpResponseRedirect("/login/")
        except Exception as e:
            messages.error(
                request, "Today Mail Sending Limit Exceeded Try After 24 Hours"
            )
            return HttpResponseRedirect("/forgot-password/")


# class ShowLeaveListView(ListView):
#     # permission_required = ('employee.can_view_employee_attendance_list',)
#     # raise_exception = True
#     model = Leave
#     template_name = "leave/fullday_leave.html"
#     def get_context_data(self, **kwargs):
#         context = super(ShowLeaveListView, self).get_context_data(**kwargs)
#         # context['object_list'] = self.model.objects.filter(user=self.request.user,status__in=[1,2,3]).order_by('-created_at')
#         context['object_list'] = self.model.objects.all().order_by('-created_at')
#         return context

# when leave delete, deducted leave from employee account again added.
def delete_leave(request):
    if request.method == "POST":
        leave_id = request.POST.get("leave_id")
        leave_user_id = request.POST.get("leave_user_id")
        leave_status = request.POST.get("leave_status")
        delete_leave = Leave.objects.filter(id=leave_id, status__in=[1, 2, 3])
        delete_leave.delete()
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        emp_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        emp_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        delta = emp_end_date - emp_start_date
        for i in range(delta.days + 1):
            delete_employee_leave = EmployeeAttendance.objects.filter(
                user_id=leave_user_id,
                date=emp_start_date + timedelta(days=i),
                empatt_leave_status__in=[5, 6],
            )
            delete_employee_leave.delete()
            get_taken_leave_unpaid = MonthlyTakeLeave.objects.filter(
                user=leave_user_id,
                year=emp_start_date.year,
                month=emp_start_date.month,
                status=2,
                leave=1,
            ).first()
            if get_taken_leave_unpaid == None:
                get_taken_leave_paid = MonthlyTakeLeave.objects.filter(
                    user=leave_user_id,
                    year=emp_start_date.year,
                    month=emp_start_date.month,
                    status=1,
                    leave=1,
                ).first()
                if get_taken_leave_paid == None:
                    get_taken_leave = MonthlyTakeLeave.objects.filter(
                        user=leave_user_id,
                        year=emp_start_date.year,
                        month=emp_start_date.month,
                        status__in=[1, 2],
                    ).order_by("-id")[:2]
                    for item in get_taken_leave:
                        item.delete()
                else:
                    get_taken_leave_paid.delete()
            else:
                get_taken_leave_unpaid.delete()
    return JsonResponse+({"status": "success"})


class EmployeeUpdateView(UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = "edit_form.html"
    success_url = reverse_lazy("")

    def form_valid(self, form, *args, **kwargs):
        profile = self.object
        profile.user.first_name = form.data["first_name"]
        profile.user.last_name = form.data["last_name"]
        if form.files.get("profile_image") == None:
            pass
        else:
            profile.profile_image = form.files.get("profile_image")
        profile.contact_no = form.data["contact_no"]
        profile.user.save()
        profile.save()
        return redirect("employee:profile")


def lead_index(request):
    project = Project.objects.all()
    return render(request, "project/lead_index.html", {"project": project})


def project_index(request):
    """
    used this to show project detail 
    """

    project = Project.objects.all()
    return render(request, "project/index.html", {"project": project})


def create_projectview(request):
    """
    used this to create a new project 
    """

    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("/project_detail")
    return render(request, "project/create.html", {"form": form})


def project_delete_view(request, pk):
    """
    used this to delete a partular project 
    """

    project = Project.objects.get(id=pk)
    project.delete()
    return HttpResponseRedirect("/project_detail")


def project_update_view(request, pk):
    """
    used this to update a particular project 
    """
    project = get_object_or_404(Project, id=pk)
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST":
        if form.is_valid():
            form.save()
        else:
            print("data not valid")
        return HttpResponseRedirect("/project_detail")
    return render(request, "project/project_update.html", {"project": project})


def client_index(request):
    """
    used to show the client detail here 
    """
    client = Client.objects.all()
    return render(request, "client/index.html", {"client": client})


def create_client_view(request):
    """
    used to create a new client 
    """
    form = ClientForm()
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("/client_detail")
    return render(request, "client/create.html", {"form": form})


def client_delete_view(request, pk):
    """
    used to delete a particular client 
    """

    client = Client.objects.get(id=pk)
    client.delete()
    return HttpResponseRedirect("/client_detail")


def client_update_view(request, pk):
    """
     used to update a particular client 
    """
    client = get_object_or_404(Client, id=pk)
    form = ClientForm(request.POST or None, instance=client)
    if request.method == "POST":
        if form.is_valid():
            form.save()
        else:
            print("data not valid")
        return HttpResponseRedirect("/client_detail")
    return render(request, "client/client_update.html", {"client": client})


def assign(request):
    """
    used to show all assigned project to user
    """
    if request.user.is_superuser:
        assign = AssignProject.objects.all()
        return render(request, "assign/assign_index.html", {"assign": assign})


def assign_project_view(request):
    """
    used to assign project from Hr to employee
    """
    if request.user.is_superuser:
        form = AssignForm()
        if request.method == "POST":
            form = AssignForm(request.POST)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect("/assign")
        return render(request, "assign/create.html", {"form": form})


def assign_delete_view(request, pk):
    """
    use this to delete a assign project
    """
    if request.user.is_superuser:
        assign = AssignProject.objects.get(id=pk)
        assign.delete()
        return HttpResponseRedirect("/assign")


def assign_update_view(request, pk):
    """
    use this to update a assign project
    """
    if request.user.is_superuser:
        assign = get_object_or_404(AssignProject, id=pk)
        form = AssignForm(request.POST or None, instance=assign)
        if request.method == "POST":
            if form.is_valid():
                form.save()
            else:
                print("data not valid")
            return HttpResponseRedirect("/assign")
        return render(request, "assign/assign_update.html", {"assign": assign})


def allemployedailyupdates(request):
    """
    use this to check all employe daily report
    """
    if request.user.is_superuser:
        if request.method == "POST":
            import pdb; pdb.set_trace();
            # project_name = request.POST["project_name__project"]
            employe_name = request.POST["value"]
            if project_name:
                daily_update = EmployeeDailyUpdate.objects.filter(
                    project_name__project__project_name=project_name
                )
            else:
                daily_update = EmployeeDailyUpdate.objects.filter(
                    project_name__employe__username=employe_name
                )
            return render(request, "daily_updates.html", {"daily_update": daily_update})
       #import pdb; pdb.set_trace();
        daily_update = EmployeeDailyUpdate.objects.all()
        employe_name = []
        for daily_updates in daily_update:
            if daily_updates.project_name.employe.username not in employe_name:
                    employe_name.append(daily_updates.project_name.employe.username)
       # import pdb; pdb.set_trace();
        return render(request, "daily_updates.html", {"daily_update": daily_update, 'employe_name':employe_name})


def employedailyupdate(request):
    """
    use this to create a report
    """
    form = EmployeeDailyUpdateForm(request.user)
    if request.method == "POST":
        form = EmployeeDailyUpdateForm(request.user, request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("/check_daily_update")
    return render(request, "employe/create_report.html", {"form": form})


def checkdailyupdate(request):
    """
    use this to check  our all daily report
    """

    # import pdb; pdb.set_trace();
    if request.method == "POST":
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        search_report = EmployeeDailyUpdate.objects.filter(
            date__range=[start_date, end_date], project_name__employe=request.user
        )
        return render(request, "employe/myreport.html", {"report": search_report})

    report = EmployeeDailyUpdate.objects.filter(project_name__employe=request.user)
    return render(request, "employe/myreport.html", {"report": report})


def editdailyreport(request, pk):
    """
    used this to edit report
    """
    edit_report = EmployeeDailyUpdate.objects.get(id=pk)
    report_date = edit_report.date
    report_week = report_date.isocalendar()[1]
    current_date = datetime.now()
    current_week = current_date.isocalendar()[1]

    form = EditDailyUpdateForm(request.POST or None, instance=edit_report)
    if request.method == "POST":
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("/check_daily_update")

    return render(
        request,
        "employe/edit_report.html",
        {
            "edit_report": edit_report,
            "report_week": report_week,
            "current_week": current_week,
        },
    )


def deletedailyreport(request, pk):
    """
    used this to delete report
    """
    report = EmployeeDailyUpdate.objects.get(id=pk)
    report.delete()
    return HttpResponseRedirect("/check_daily_update")
