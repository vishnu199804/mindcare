from django.urls import path
from . import views

urlpatterns = [

    # ===============================
    # 📅 APPOINTMENTS
    # ===============================

    path("book/", views.book_appointment, name="book_appointment"),
    path("my/", views.patient_appointments, name="patient_appointments"),
    path("doctor/", views.doctor_appointments, name="doctor_appointments"),

    # ===============================
    # ✅ APPROVE / ❌ REJECT
    # ===============================
    path("approve/<int:id>/", views.approve_appointment, name="approve_appointment"),
    path("reject/<int:id>/", views.reject_appointment, name="reject_appointment"),

    # ===============================
    # 💳 PAYMENT
    # ===============================
    
    path("pay/<int:appointment_id>/", views.pay_appointment, name="pay_appointment"),
    path("razorpay/success/", views.razorpay_success, name="razorpay_success"),
    path("payment-success/<int:appointment_id>/",views.payment_success,name="payment_success",),
    
    # ===============================
    # 🎥 VIDEO CALL
    # ===============================

    path("join/<int:appointment_id>/", views.join_call, name="join_call"),

    # ===============================
    # 🧾 PRESCRIPTIONS
    # ===============================
    
    path("prescription/write/<int:appointment_id>/",views.write_prescription,name="write_prescription",),
    path("prescription/view/<int:appointment_id>/",views.view_prescription,name="view_prescription",),
    path("prescription/edit/<int:appointment_id>/",views.edit_prescription,name="edit_prescription",),
    path("prescription/download/<int:appointment_id>/",views.download_prescription,name="download_prescription",),

    # ===============================
    # 👨‍⚕️ DOCTOR DASHBOARD
    # ===============================
    
    path("doctor/earnings/", views.doctor_earnings, name="doctor_earnings"),
    path("doctor/prescriptions/",views.doctor_prescriptions,name="doctor_prescriptions",),
    path("prescription/download-redirect/<int:appointment_id>/",views.download_redirect,name="download_redirect",),
]