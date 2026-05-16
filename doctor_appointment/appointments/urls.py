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
 path('book/<int:pk>/', views.book_appointment, name='book_appointment'),
    path('notifications/', views.notifications_page, name='notifications_page'),
    path('my_appointments/', views.my_appointments, name='my_appointments'),
path('upload/<int:appointment_id>/',views.upload_prescription, name='upload_prescription'),
    path('doctor_appointments/', views.doctor_appointments,name='doctor_appointments'),
    path('update-status/', views.update_appointment_status,name='update_appointment_status'),
    path('admin-appointments/', views.admin_appointments, name='admin_appointments'),
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment_admin, name='cancel_appointment_admin'),
    path('patient-cancel/<int:appointment_id>/', views.cancel_appointment_patient, name='cancel_appointment_patient'),

]
