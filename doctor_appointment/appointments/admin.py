from django.contrib import admin

from .models import Appointment, Notification, Prescription

# Register your models here.
admin.site.register(Appointment)
admin.site.register(Notification)
admin.site.register(Prescription)