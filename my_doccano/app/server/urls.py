"""app URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from  django.contrib.auth import views as auth_views
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from server.views import (UsernameCountView, MobileCountView, UserView, Register)

urlpatterns = [
    url(r'^authorizations/$', obtain_jwt_token),
    url(r'^usernames/(?P<username>\w{1,20})/count/$', UsernameCountView.as_view()),
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', MobileCountView.as_view()),
    url(r'^(?P<mobile>1[3-9]\d{9})/count/$', MobileCountView.as_view()),
    url(r'^users/$', UserView.as_view()),
    url(r'^register/$', Register.as_view()),
    # path('login/', LoginView.as_view(), name='login'),
]
