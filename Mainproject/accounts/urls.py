"""Mainproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from accounts.views import (register_home,register,loginview,logoutview,add_collegue_detail,
    add_collegue_home,add_collegue,confirm_success,collegue_list,collegue_sorted_list,collegue_detail,my_account,
                            test,change_password)

urlpatterns = [
    path('register_home/', register_home, name='register home'),
    path('register/',register, name='register'),
    path('login/', loginview, name='login'),
    path('logout/', logoutview, name='logout'),
    path('add_collegue_home/', add_collegue_home, name='add collegue home'),
    path('add_collegue/', add_collegue, name='add collegue'),
    path('add_collegue_detail/', add_collegue_detail, name='add collegue detail'),
    path('confirm_sucess/', confirm_success, name='confirm success'),
    path('collegue_list/', collegue_list, name='collegue list'),
    path('collegue_sorted_list/', collegue_sorted_list, name='collegue sorted list'),
    path('collegue_detail/', collegue_detail, name='collegue detail'),
    path('my_account/', my_account, name='my account'),
    path('change_password/', change_password, name='change password'),
    path('test/',test, name='test')
]
