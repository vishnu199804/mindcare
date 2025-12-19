from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Appointment(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("completed", "Completed"),
    )

    PAYMENT_STATUS = (
        ("unpaid", "Unpaid"),
        ("paid", "Paid"),
    )

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="patient_appointments"
    )

    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="doctor_appointments"
    )

    date = models.DateTimeField()
    reason = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="unpaid"
    )

    # ===============================
    # 💻 VIDEO CALL
    # ===============================
    meeting_link = models.URLField(
        blank=True,
        null=True
    )

    # ===============================
    # 🧾 ONLINE PRESCRIPTION (NO PDF UPLOAD)
    # ===============================
    patient_age = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    patient_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Weight in KG"
    )

    diagnosis = models.TextField(
        blank=True,
        help_text="Doctor diagnosis"
    )

    medicines = models.TextField(
        blank=True,
        help_text="Medicine name, dosage, frequency"
    )

    advice = models.TextField(
        blank=True,
        help_text="Doctor advice"
    )

    prescription_created = models.BooleanField(
        default=False
    )

    # ===============================
    # 💳 PAYMENT (RAZORPAY)
    # ===============================
    razorpay_order_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} → {self.doctor} on {self.date}"
