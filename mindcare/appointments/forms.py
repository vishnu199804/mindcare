from django import forms
from django.contrib.auth import get_user_model
from .models import Appointment

User = get_user_model()

class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=User.objects.filter(role="doctor"),
        label="Choose Doctor"
    )

    date = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'reason']
