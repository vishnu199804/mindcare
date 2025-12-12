from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment


# --------------------------
# DOCTOR DASHBOARD VIEW
# --------------------------
@login_required
def doctor_dashboard(request):
    doctor = request.user

    # Get appointments belonging to this doctor
    pending = Appointment.objects.filter(doctor=doctor, status="pending").order_by("-date")
    approved = Appointment.objects.filter(doctor=doctor, status="approved").order_by("-date")
    rejected = Appointment.objects.filter(doctor=doctor, status="rejected").order_by("-date")

    # Also get all for listing table
    all_appointments = Appointment.objects.filter(doctor=doctor).order_by("-date")

    return render(request, "dashboard/doctor_dashboard.html", {
        "pending_appointments": pending,
        "approved_appointments": approved,
        "rejected_appointments": rejected,

        "pending_count": pending.count(),
        "approved_count": approved.count(),
        "rejected_count": rejected.count(),

        "appointments": all_appointments,
    })

# --------------------------
# PATIENT DASHBOARD VIEW
# --------------------------
@login_required
def patient_dashboard(request):
    patient = request.user

    appointments = Appointment.objects.filter(patient=patient).order_by('-date')

    return render(request, "dashboard/patient_dashboard.html", {
        "appointments": appointments
    })