from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment, Notification, Prescription
from accounts.models import DoctorProfile
from datetime import date, timedelta
from django.db.models import F
from django.views.decorators.http import require_POST


@login_required
def book_appointment(request, pk):

    doctor = get_object_or_404(DoctorProfile, pk=pk)

    today = date.today()

    # Maximum booking date = tomorrow
    max_booking_date = today + timedelta(days=1)

    if request.method == "POST":

        selected_date = request.POST.get("appointment_date")

        # No date selected
        if not selected_date:
            return render(request, "doctor_detail.html", {
                "doctor": doctor,
                "error": "Please select an appointment date.",
                "today": today,
                "max_booking_date": max_booking_date
            })

        selected_date = date.fromisoformat(selected_date)

        # Prevent past dates
        if selected_date < today:
            return render(request, "doctor_detail.html", {
                "doctor": doctor,
                "error": "Cannot book past dates.",
                "today": today,
                "max_booking_date": max_booking_date
            })

        # Prevent booking beyond tomorrow
        if selected_date > max_booking_date:
            return render(request, "doctor_detail.html", {
                "doctor": doctor,
                "error": "You can only book for today or tomorrow.",
                "today": today,
                "max_booking_date": max_booking_date
            })

        # Prevent duplicate booking
        already_booked = Appointment.objects.filter(
            patient=request.user,
            doctor=doctor,
            appointment_date=selected_date
        ).exclude(status="CANCELLED").exists()

        if already_booked:
            return render(request, "doctor_detail.html", {
                "doctor": doctor,
                "error": "You already booked this doctor for this date.",
                "today": today,
                "max_booking_date": max_booking_date
            })

        # Appointments for selected date
        day_appointments = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=selected_date
        ).exclude(status='CANCELLED')

        # Daily limit
        if day_appointments.count() >= 20:

            return render(request, "doctor_detail.html", {
                "doctor": doctor,
                "error": "Appointment limit reached for this date.",
                "today": today,
                "max_booking_date": max_booking_date
            })

        # Queue logic
        last_appt = day_appointments.order_by('-queue_position').first()

        if last_appt:
            next_position = last_appt.queue_position + 1
        else:
            next_position = 1

        # Create appointment
        appointment = Appointment.objects.create(
            patient=request.user,
            doctor=doctor,
            appointment_date=selected_date,
            token_number=next_position,
            queue_position=next_position
        )

        # Notification
        Notification.objects.create(
            user=request.user,
            message=f"Appointment booked with Dr. {doctor.name} for {selected_date}. Token #{appointment.token_number}"
        )

        return redirect("my_appointments")

    return render(request, "doctor_detail.html", {
        "doctor": doctor,
        "today": today,
        "max_booking_date": max_booking_date
    })


@login_required
def my_appointments(request):

    appointments = Appointment.objects.filter(
        patient=request.user
    ).order_by('-created_at')

    all_today_appointments = Appointment.objects.exclude(
        status="CANCELLED"
    )

    return render(request, "my_appointments.html", {
        "appointments": appointments,
        "all_today_appointments": all_today_appointments
    })


@login_required
def notifications_page(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    notifications.update(is_read=True)

    return render(request, "notifications.html", {
        "notifications": notifications
    })


@login_required
def doctor_appointments(request):
    doctor = request.user.doctorprofile

    appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=date.today()
    ).exclude(status='CANCELLED').order_by('queue_position')

    return render(request, 'doctor_appointments.html', {
        'appointments': appointments
    })

@login_required
def upload_prescription(request, appointment_id):
    doctor = request.user.doctorprofile

    appointment = Appointment.objects.get(
        id=appointment_id,
        doctor=doctor
    )

    if request.method == "POST":
        file = request.FILES.get('file')

        Prescription.objects.create(
            appointment=appointment,
            doctor=doctor,
            patient=appointment.patient.patientprofile,
            file=file
        )

        return redirect('doctor_appointments')

    return render(request, 'upload_prescription.html', {
        'appointment': appointment
    })


@login_required
@require_POST
def update_appointment_status(request):

    doctor = request.user.doctorprofile

    appointment_id = request.POST.get("appointment_id")
    new_status = request.POST.get("status")

    appointment = Appointment.objects.get(
        id=appointment_id,
        doctor=doctor
    )

    # If doctor marks one ONGOING,
    # remove ongoing from others first
    if new_status == "ONGOING":

        Appointment.objects.filter(
            doctor=doctor,
            appointment_date=date.today(),
            status="ONGOING"
        ).update(status="WAITING")

    appointment.status = new_status
    appointment.save()

    return redirect("doctor_appointments")


@login_required
def admin_appointments(request):

    # Only admin can access
    if not request.user.is_superuser:
        return redirect("home")

    appointments = Appointment.objects.all().order_by('-created_at')

    return render(request, 'admin_appointments.html', {
        'appointments': appointments
    })



@login_required
@require_POST
def cancel_appointment_admin(request, appointment_id):

    # Only admin
    if not request.user.is_superuser:
        return redirect("home")

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    # Only pending appointments can be cancelled
    if appointment.status == "WAITING":

        appointment.status = "CANCELLED"
        appointment.save()

    return redirect("admin_appointments")


@login_required
@require_POST
def cancel_appointment_patient(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=request.user
    )

    # Only waiting appointments can be cancelled
    if appointment.status != "WAITING":
        return redirect("my_appointments")

    old_queue_position = appointment.queue_position

    # Mark as cancelled
    appointment.status = "CANCELLED"
    appointment.save()

    # Shift queue positions
    Appointment.objects.filter(
        doctor=appointment.doctor,
        appointment_date=appointment.appointment_date,
        queue_position__gt=old_queue_position
    ).exclude(
        status="CANCELLED"
    ).update(
        queue_position=F('queue_position') - 1
    )

    return redirect("my_appointments")


