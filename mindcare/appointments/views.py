from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from .models import Appointment
from .forms import AppointmentForm
import razorpay


# ============ APPOINTMENTS ============

@login_required
def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            return redirect("patient_dashboard")
    else:
        form = AppointmentForm()

    return render(request, "appointments/book_appointment.html", {"form": form})


@login_required
def doctor_appointments(request):
    appointments = Appointment.objects.filter(doctor=request.user).order_by("date")
    return render(request, "appointments/doctor_appointments.html", {"appointments": appointments})


@login_required
def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, "appointments/appointment_list.html", {"appointments": appointments})


@login_required
def approve_appointment(request, id):
    appt = get_object_or_404(Appointment, id=id)
    appt.status = "approved"
    appt.save()
    return redirect("doctor_appointments")


@login_required
def reject_appointment(request, id):
    appt = get_object_or_404(Appointment, id=id)
    appt.status = "rejected"
    appt.save()
    return redirect("doctor_appointments")


# ============ PAYMENT USING RAZORPAY ============

@login_required
def pay_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    payment = client.order.create({
        "amount": 50000,  # 500 INR
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


@csrf_exempt
def razorpay_success(request):
    if request.method == "POST":
        data = request.POST

        order_id = data.get("razorpay_order_id")
        payment_id = data.get("razorpay_payment_id")
        signature = data.get("razorpay_signature")

        appointment = Appointment.objects.get(razorpay_order_id=order_id)

        appointment.payment_status = "paid"
        appointment.razorpay_payment_id = payment_id
        appointment.razorpay_signature = signature
        appointment.save()

        return redirect("payment_success", appointment_id=appointment.id)

    return redirect("patient_dashboard")


@login_required
def payment_success(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    return render(request, "appointments/payment_success.html", {
        "appointment": appointment
    })
