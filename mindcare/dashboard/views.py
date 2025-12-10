from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment


# --------------------------
# DOCTOR DASHBOARD VIEW
# --------------------------
@login_required
def doctor_dashboard(request):
    doctor = request.user

    pending = Appointment.objects.filter(doctor=doctor, status="pending")
    approved = Appointment.objects.filter(doctor=doctor, status="approved")

    return render(request, "dashboard/doctor_dashboard.html", {
        "pending_appointments": pending,
        "approved_appointments": approved,
        "pending_count": pending.count(),
        "approved_count": approved.count(),
    })


# --------------------------
# PATIENT DASHBOARD VIEW
# --------------------------
@login_required
def patient_dashboard(request):
    user = request.user

    appointments = Appointment.objects.filter(patient=user).order_by('-date')

    return render(request, "dashboard/patient_dashboard.html", {
        "appointments": appointments
    })
