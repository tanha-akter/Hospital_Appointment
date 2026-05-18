from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm

from appointments.models import Appointment


@login_required
def add_review(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    # ek matro patient e review korte parbe
    if request.user != appointment.patient:
        return redirect('home')

    # appointment ek matro complete hole jabe
    if appointment.status != "COMPLETED":
        return redirect('my_appointments')

    # keu duplicate review dite parbena
    if hasattr(appointment, 'review'):
        return redirect('my_appointments')

    if request.method == 'POST':

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.patient = appointment.patient.patientprofile
            review.doctor = appointment.doctor
            review.appointment = appointment

            review.save()

            return redirect('doctor_detail', pk=appointment.doctor.id)

    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {
        'form': form,
        'appointment': appointment
    })