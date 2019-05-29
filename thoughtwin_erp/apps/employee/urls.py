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
    path('emplist/', views.EmployeeListView.as_view(), name='employee_list'),
    #url(r'^books/(?P<pk>\d+)/delete/$', views.book_delete, name='book_delete'),
    path('deactivate/<int:pk>/', deactivate_user,name='deactivate-user'),
    path('delete_record/', delete_record, name='delete_record'),
    # path('edit/<int:id>/', edit, name='edit'),
    # path('update/<int:id>', update, name='update'),
    # url('users/(?P<pk>)/edit/$', EditUserProfileView.as_view(), name="edit-user-profile"),
    path('users/<int:pk>/', views.EditUserProfileView.as_view(), name="edit-user-profile"),
    
    # path('person/json/', person_json, name='person_json'),
    


]