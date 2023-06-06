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
from django.urls import path,include
from eggs import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('',views.home,name='home'),
    path('select/', views.select,name='select'),
    path('chicks_menu/', views.chicks_menu,name='chicks_menu'),
    path('eggs_menu/', views.eggs_menu,name='eggs_menu'),
    path('new_batch/', views.new_batch,name='chicks_new_batch'),
    path('update_chicks/', views.update_batch,name='update_batch'),
    path('feed_input/',views.feed_input,name='feed_input'),
    path('chicks_input/',views.chicks_input,name='chicks_input'),
    path('move_batch/',views.move_batch,name='move_batch'),
    path('feed_input_hens/',views.update_feed_hens,name='feed_input_hens'),
    path('eggs_input_hens/',views.update_eggs_hens,name='eggs_input_hens'),
    path('delivery_input_hens/',views.update_delivery_hens,name='delivery_input_hens'),
    path('success/', views.success,name='success'),
    path('close_production/',views.close_production,name='close_production'),

    path('add_user/', views.add_user, name='add_user'),
    path('admin_report/',views.admin_menu,name='admin_report'),
    path('layer_report/',views.layer_report,name='layer_report'),
]
