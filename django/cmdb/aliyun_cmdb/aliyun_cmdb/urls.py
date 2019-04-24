"""aliyun_cmdb URL Configuration

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
from django.urls import path
from information import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('index/', views.index, name='index'),
    path('project_info/',views.project_info , name='project_info'),
    path('project_del/<int:pk>/',views.project_del , name='project_del'),
    path('project_edit/<int:pk>/',views.project_edit , name='project_edit'),
    path('rds_info/', views.rds_info, name='rds_info'),
    path('project_data/<int:pk>/',views.project_data , name='project_data'),
    path('ecs_info/', views.ecs_info, name='ecs_info'),
    path('ecs_detail/<str:p_name>', views.ecs_detail, name='ecs_detail'),
    path('ecs_start/', views.ecs_start, name='ecs_start'),
    path('ecs_stop/', views.ecs_stop, name='ecs_stop'),
    path('ecs_restart/', views.ecs_restart, name='ecs_restart'),
    path('ecs_reset/', views.ecs_reset, name='ecs_reset'),
    path('form_test/',views.form_test),
]
