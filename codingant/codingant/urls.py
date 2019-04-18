"""codingant URL Configuration

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
    1. Import the static() function: from django.urls import static, path
    2. Add a URL to urlpatterns:  path('blog/', static('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

import employees
from codingant import settings
from employees.forms import LoginForm

urlpatterns = [
    path('employees/', include('employees.urls')),
    # https://www.jianshu.com/p/9deb5cfcaca8    讲解django内置登录框架LoginView.as_view
    path('accounts/login/', auth_views.LoginView.as_view(authentication_form=LoginForm), name='login'),
    path('accounts/employee_profile/', employees.views.employee_profile, name='employee_profile'),
    path('accounts/profile/', employees.views.profile, name='profile'),
    path('accounts/signout/', employees.views.logout_view, name="account-sign-out"),
    path('accounts/timesheet/', employees.views.timesheet, name='timesheet'),
    path('admin/interview_resume/<int:pk>/', employees.views.interview_resume, name='interview_resume'),
    path('admin/', admin.site.urls),
    path('', employees.views.home),
    path('accounts/change_password/', employees.views.changepwd, name='change-password'),
    path('face/', include('face_login.urls')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
