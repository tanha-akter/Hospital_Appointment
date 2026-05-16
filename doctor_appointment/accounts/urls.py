"""
URL configuration for doctor_appointment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from .import views

urlpatterns = [
    path('create_account/', views.register_view, name='create_account'),
    path('login/', views.login_view, name='login'),
    path('patient_profile/', views.patient_profile, name='patient_profile'),
    path('doctor_profile/', views.doctor_profile, name='doctor_profile'),
    path('logout/', views.logout_view, name='logout'),
]
