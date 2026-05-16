from django.db import models
from accounts.models import DoctorProfile, PatientProfile
from appointments.models import Appointment


class Review(models.Model):

    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField(choices=RATING_CHOICES)

    review_text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.user.username} -> {self.doctor.user.username}"