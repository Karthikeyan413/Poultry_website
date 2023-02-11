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
    path('admin/', admin.site.urls),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('',views.home,name='home'),
    path('select/', views.select,name='select'),
    path('chicks_menu/', views.chicks_menu,name='chicks_menu'),
    # path('eggs_input/', views.eggs_input,name='eggs_input'),
    path('new_batch/', views.new_batch,name='chicks_new_batch'),
    path('update_chicks/', views.update_batch,name='update_batch'),
    path('feed_input/',views.feed_input,name='feed_input'),
    path('chicks_input/',views.chicks_input,name='chicks_input'),
    path('move_batch/',views.move_batch,name='move_batch'),
    # path('batch_layer/', views.batch_layer,name='batch_layer'),
    # path(r'check/(?P<batch_id>[0-9]+)/$', views.check, name='check'),
    # path('display/', views.display,name='display'),
]
