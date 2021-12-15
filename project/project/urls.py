"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from app import views as core_views
from django.urls import path

urlpatterns = [
    path('', core_views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name = 'app/login.html'), name='login'),
    path(r'logout/', auth_views.LogoutView.as_view(next_page = 'login'), name='logout'),
    path(r'signup/', core_views.signup, name='signup'),
    path(r'account_activation_sent/', core_views.account_activation_sent, name='account_activation_sent'),
    path(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
      core_views.activate, name='activate'),
]