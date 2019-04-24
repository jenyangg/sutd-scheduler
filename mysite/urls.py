"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from users import views as user_views
from formstoadmin import views as formstoadminViews
from schedule import views as scheduleViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('schedule.urls')),  # if path is empty, it's the homepage
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name='logout'),
    path('requestform/', include('formstoadmin.urls')),
    # '' contains string after /requestform
    path('request-form', formstoadminViews.ScheduleRequest, name='request-form'),
    path('input-module-info', formstoadminViews.inputModule, name='input-module-info'),
    path('view-requests/', formstoadminViews.viewRequests, name='view-requests'),
    path('add-event/', formstoadminViews.addEvent, name='add-event'),
    path('generate-schedule/', scheduleViews.generateSchedule, name="generate-schedule"),
    path('module-upload/', formstoadminViews.moduleUpload, name="module-upload"),
    path('input-class-info/', formstoadminViews.InputClassInfo.as_view(), name="input-class-info"),
    path('runAlgo/',scheduleViews.runAlgo),
    re_path(r'^return_data/(?P<Classs>[^/]+)/(?P<modyews>[^/]+)/$',scheduleViews.return_data),
    re_path(r'^return_data/(?P<Classs>[^/]+)/$',scheduleViews.return_data),
    re_path(r'^return_data/$',scheduleViews.return_data),
    path('gcalExport/',scheduleViews.gcalExport),
]