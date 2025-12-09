
from django.shortcuts import render
from appointments.models import Appointment, Prescription, Payment, MoodLog
from django.contrib.auth.decorators import login_required

@login_required
def doctor_dashboard(request):
    doctor = request.user

    pending_appointments = Appointment.objects.filter(doctor=doctor, status="pending")
    approved_appointments = Appointment.objects.filter(doctor=doctor, status="approved")

    prescriptions = Prescription.objects.filter(doctor=doctor).order_by('-created_at')

    payments = Payment.objects.all()  # You can filter if needed

    moods = MoodLog.objects.all().order_by('-date')

    patient_list = Appointment.objects.filter(doctor=doctor).values('patient__username').distinct()

    return render(request, "dashboard/doctor_dashboard.html", {
        "pending_appointments": pending_appointments,
        "approved_appointments": approved_appointments,
        "prescriptions": prescriptions,
        "payments": payments,
        "moods": moods,
        "patient_list": patient_list,
        "pending_count": pending_appointments.count(),
        "today_patients": approved_appointments.count(),
        "prescription_count": prescriptions.count(),
    })
@login_required
def patient_dashboard(request):
    user = request.user

    appointments = Appointment.objects.filter(patient=user).order_by('-date')

    mood_logs = MoodLog.objects.filter(patient=user).order_by('-date')[:7]

    return render(request, "dashboard/patient_dashboard.html", {
        "appointments": appointments,
        "mood_logs": mood_logs,
    })