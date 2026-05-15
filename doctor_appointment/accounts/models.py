from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
#Custom user model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


# patient profile
class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=10,
        choices=[
            ('MALE', 'Male'),
            ('FEMALE', 'Female'),
            ('OTHER', 'Other'),
        ]
    )

    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='patients/', blank=True)

    def __str__(self):
        return self.full_name




# doctor profile
class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    experience = models.IntegerField()
    address = models.TextField()
    fees = models.IntegerField()
    about = models.TextField()
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='doctors/', blank=True)

    def __str__(self):
        return self.name