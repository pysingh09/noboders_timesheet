from django.urls import path
from employee.views import * 
from . import views
app_name = 'employee'

urlpatterns = [
    # path('dashboard', Dashboard.as_view(), name='dashboard' ),
    path('signup/', signup, name='signup'),
    path('home/', home, name='home'),
    path('profile/', employee_profile, name='profile'),
    path('file/', file_upload, name='file_upload'),
    path('employeelist/', views.EmployeeListView.as_view(), name='employee_list'),
    path('deactivate/<int:pk>/', deactivate_user,name='deactivate-user'),
    path('delete_record/', delete_record, name='delete_record'), 
    path('update/<int:pk>/', views.EditProfileView.as_view(), name="update"),
    # path('person/json/', person_json, name='person_json'),
    


]