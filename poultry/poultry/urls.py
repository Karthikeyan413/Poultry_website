"""poultry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from eggs import views


urlpatterns = [
    path('admin/',admin.site.urls,name='login_admin'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('',views.home,name='home'),
    path('batch_layer/', views.batch_layer,name='batch_layer'),
    path(r'check/(?P<batch_id>[0-9]+)/$', views.check, name='check'),
    path('input/', views.eggs_input,name='input'),
    path('display/', views.display,name='display'),
     path('success/', views.success,name='success'),
]
