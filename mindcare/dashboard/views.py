from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment


# ==========================
# DOCTOR DASHBOARD
# ==========================

@login_required
def doctor_dashboard(request):
    if request.user.role != "doctor":
        return redirect("patient_dashboard")

    doctor = request.user

    pending = Appointment.objects.filter(doctor=doctor, status="pending").order_by("-date")
    approved = Appointment.objects.filter(doctor=doctor, status="approved").order_by("-date")
    rejected = Appointment.objects.filter(doctor=doctor, status="rejected").order_by("-date")

    all_appointments = Appointment.objects.filter(doctor=doctor).order_by("-date")

    return render(request, "dashboard/doctor_dashboard.html", {
        "pending_appointments": pending,
        "approved_appointments": approved,
        "rejected_appointments": rejected,
        "appointments": all_appointments,
        "pending_count": pending.count(),
        "approved_count": approved.count(),
        "rejected_count": rejected.count(),
    })


# ==========================
# PATIENT DASHBOARD
# ==========================

@login_required
def patient_dashboard(request):
    if request.user.role != "patient":
        return redirect("doctor_dashboard")

    appointments = Appointment.objects.filter(
        patient=request.user
    ).order_by("-date")

    next_appt = appointments.filter(status__in=["pending", "approved"]).first()

    # 💰 CALCULATIONS
    paid_appointments = appointments.filter(payment_status="paid")
    total_spent = paid_appointments.count() * 500  # ₹500 per appointment
    balance = 0  # placeholder (future wallet feature)

    context = {
        "appointments": appointments,
        "next_appt": next_appt,
        "total_spent": total_spent,
        "balance": balance,
    }

    return render(request, "dashboard/patient_dashboard.html", context)

# ==========================
# ROLE BASED REDIRECT
# ==========================

@login_required
def dashboard_redirect(request):
    if request.user.role == "doctor":
        return redirect("doctor_dashboard")
    return redirect("patient_dashboard")
