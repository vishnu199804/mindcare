from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .models import Appointment
import razorpay
import uuid

User = get_user_model()

# =====================================================
# 📅 BOOK APPOINTMENT (PATIENT)
# =====================================================

@login_required
def book_appointment(request):
    if request.user.role != "patient":
        return redirect("doctor_dashboard")

    if request.method == "POST":
        doctor_id = request.POST.get("doctor")
        date = request.POST.get("date")

        doctor = get_object_or_404(User, id=doctor_id, role="doctor")

        Appointment.objects.create(
            patient=request.user,
            doctor=doctor,
            date=date
        )
        return redirect("patient_dashboard")

    doctors = User.objects.filter(role="doctor")
    return render(request, "appointments/book.html", {"doctors": doctors})


# =====================================================
# 👤 PATIENT APPOINTMENTS
# =====================================================

@login_required
def patient_appointments(request):
    appointments = Appointment.objects.filter(
        patient=request.user
    ).order_by("-date")

    return render(request, "appointments/appointment_list.html", {
        "appointments": appointments
    })


# =====================================================
# 🧑‍⚕️ DOCTOR APPOINTMENTS
# =====================================================

@login_required
def doctor_appointments(request):
    if request.user.role != "doctor":
        return redirect("patient_dashboard")

    appointments = Appointment.objects.filter(
        doctor=request.user
    ).order_by("-date")

    paid_count = appointments.filter(payment_status="paid").count()
    total_earnings = paid_count * 500

    return render(request, "appointments/doctor_appointments.html", {
        "appointments": appointments,
        "paid_count": paid_count,
        "total_earnings": total_earnings,
    })

# =====================================================
# ✅ APPROVE / ❌ REJECT
# =====================================================

@login_required
def approve_appointment(request, id):
    appt = get_object_or_404(Appointment, id=id, doctor=request.user)
    appt.status = "approved"
    appt.save()
    return redirect("doctor_dashboard")


@login_required
def reject_appointment(request, id):
    appt = get_object_or_404(Appointment, id=id, doctor=request.user)
    appt.status = "rejected"
    appt.save()
    return redirect("doctor_dashboard")


# =====================================================
# 💳 PAYMENT
# =====================================================

@login_required
def pay_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=request.user,
        status="approved"
    )

    client = razorpay.Client(auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    ))

    payment = client.order.create({
        "amount": 500,
        "currency": "INR",
        "payment_capture": "1"
    })

    appointment.razorpay_order_id = payment["id"]
    appointment.save()

    return render(request, "appointments/pay.html", {
        "appointment": appointment,
        "payment": payment,
        "RAZORPAY_KEY_ID": settings.RAZORPAY_KEY_ID
    })

# =====================================================
# 💳 RAZORPAY SUCCESS
# =====================================================

@csrf_exempt
def razorpay_success(request):
    if request.method == "POST":
        appointment = get_object_or_404(
            Appointment,
            razorpay_order_id=request.POST.get("razorpay_order_id")
        )

        appointment.payment_status = "paid"

        if not appointment.meeting_link:
            appointment.meeting_link = (
                f"https://meet.jit.si/MindCare-{uuid.uuid4().hex[:12]}"
            )

        appointment.save()
        return redirect("payment_success", appointment_id=appointment.id)

    return redirect("patient_dashboard")


@login_required
def payment_success(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, "appointments/payment_success.html", {
        "appointment": appointment
    })


# =====================================================
# 🎥 JOIN VIDEO CALL
# =====================================================

@login_required
def join_call(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user not in [appointment.patient, appointment.doctor]:
        return redirect("home")

    if appointment.payment_status != "paid":
        return redirect("patient_dashboard")

    return redirect(appointment.meeting_link)


# =====================================================
# 🧾 WRITE PRESCRIPTION (DOCTOR)
# =====================================================

@login_required
def write_prescription(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=request.user,
        payment_status="paid"
    )

    if request.method == "POST":
        appointment.patient_age = request.POST.get("patient_age")
        appointment.patient_weight = request.POST.get("patient_weight")
        appointment.diagnosis = request.POST.get("diagnosis")
        appointment.medicines = request.POST.get("medicines")
        appointment.advice = request.POST.get("advice")

        appointment.prescription_created = True
        appointment.status = "completed"
        appointment.save()

        return redirect("doctor_prescriptions")

    return render(request, "appointments/write_prescription.html", {
        "appointment": appointment
    })


# =====================================================
# 👀 VIEW PRESCRIPTION (PATIENT + DOCTOR)
# =====================================================

@login_required
def view_prescription(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        prescription_created=True
    )

    if request.user not in [appointment.patient, appointment.doctor]:
        return redirect("home")

    return render(request, "appointments/view_prescription.html", {
        "appointment": appointment
    })


# =====================================================
# ✏️ EDIT PRESCRIPTION (DOCTOR ONLY)
# =====================================================

@login_required
def edit_prescription(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=request.user,
        prescription_created=True
    )

    if request.method == "POST":
        appointment.patient_age = request.POST.get("patient_age")
        appointment.patient_weight = request.POST.get("patient_weight")
        appointment.diagnosis = request.POST.get("diagnosis")
        appointment.medicines = request.POST.get("medicines")
        appointment.advice = request.POST.get("advice")
        appointment.save()

        return redirect("doctor_prescriptions")

    return render(request, "appointments/edit_prescription.html", {
        "appointment": appointment
    })


# =====================================================
# 💰 DOCTOR EARNINGS
# =====================================================

@login_required
def doctor_earnings(request):
    if request.user.role != "doctor":
        return redirect("patient_dashboard")

    appointments = Appointment.objects.filter(
        doctor=request.user,
        payment_status="paid"
    )

    total_earnings = appointments.count() * 500

    return render(request, "appointments/doctor_earnings.html", {
        "appointments": appointments,
        "total_earnings": total_earnings
    })


# =====================================================
# 📄 DOCTOR PRESCRIPTIONS LIST
# =====================================================

@login_required
def doctor_prescriptions(request):
    if request.user.role != "doctor":
        return redirect("patient_dashboard")

    prescriptions = Appointment.objects.filter(
        doctor=request.user,
        prescription_created=True
    ).order_by("-date")

    return render(request, "appointments/doctor_prescriptions.html", {
        "prescriptions": prescriptions
    })

# =====================================================
# ⬇️ DOWNLOAD PRESCRIPTION (PATIENT)
# =====================================================

@login_required
def download_redirect(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user not in [appointment.patient, appointment.doctor]:
        return redirect("home")

    return render(
        request,
        "appointments/download_redirect.html",
        {"appointment": appointment}
    )


@login_required
def download_prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=prescription.pdf"

    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    y = height - 50
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "MindCare - Medical Prescription")

    y -= 40
    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Doctor: {appointment.doctor.username}")
    y -= 20
    p.drawString(50, y, f"Patient: {appointment.patient.username}")
    y -= 20
    p.drawString(50, y, f"Age: {appointment.patient_age}")
    y -= 20
    p.drawString(50, y, f"Weight: {appointment.patient_weight} KG")

    y -= 30
    p.drawString(50, y, "Diagnosis:")
    y -= 20
    p.drawString(70, y, appointment.diagnosis)

    y -= 30
    p.drawString(50, y, "Medicines:")
    y -= 20
    p.drawString(70, y, appointment.medicines)

    y -= 30
    p.drawString(50, y, "Advice:")
    y -= 20
    p.drawString(70, y, appointment.advice)

    p.showPage()
    p.save()

    return response
@login_required
def download_redirect(request, appointment_id):
    """
    Download PDF and auto-redirect back
    """
    response = download_prescription(request, appointment_id)

    # Auto redirect after download
    response["Refresh"] = "2; url=/appointment/doctor/prescriptions/"

    return response