from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['guest_name', 'check_in', 'check_out', 'room_number', 'floor_number']
        widgets = {
            'check_in': forms.TextInput(attrs={'type': 'date'}),
            'check_out': forms.TextInput(attrs={'type': 'date'})
        }