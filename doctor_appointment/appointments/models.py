from django.db import models
from accounts.models import User, DoctorProfile, PatientProfile


class Appointment(models.Model):

    STATUS_CHOICES = [
        ('WAITING', 'Waiting'),
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
        ('NOT_PRESENT', 'Not Present'),
        ('MISSED', 'Missed'),
        ('CANCELLED', 'Cancelled'),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)

    appointment_date = models.DateField(null=True, blank=True)

    token_number = models.IntegerField()
    queue_position = models.IntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='WAITING'
    )

    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)

    file = models.FileField(upload_to='prescriptions/')
    created_at = models.DateTimeField(auto_now_add=True)