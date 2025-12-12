from django.urls import path
from . import views

urlpatterns = [

    # Appointment
    path("book/", views.book_appointment, name="book_appointment"),
    path("doctor/", views.doctor_appointments, name="doctor_appointments"),
    path("", views.appointment_list, name="appointment_list"),
    path("appointment/<int:id>/approve/", views.approve_appointment, name="approve_appointment"),
    path("appointment/<int:id>/reject/", views.reject_appointment, name="reject_appointment"),

    # Payment
    path('pay/<int:appointment_id>/', views.pay_appointment, name='pay_appointment'),
    path('payment/success/<int:appointment_id>/', views.payment_success, name='payment_success'),
    path('razorpay/callback/', views.razorpay_success, name='razorpay_callback'),]
