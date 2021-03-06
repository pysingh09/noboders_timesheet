"""thoughtwin_erp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
# from employee.views import EmailLoginForm
# from django.contrib.auth import views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import views as auth_views
# from django.contrib.auth.views import login

# from django.contrib.auth.decorators import user_passes_test


# login_forbidden =  user_passes_test(lambda u: u.is_anonymous(), '/')




urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('employee.urls', namespace='employee')),
    # path('login/', auth_views.login, name='login'),
    
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
]
