from django import forms
from .models import Booking
from trucks.models import Extra

class BookingForm(forms.ModelForm):
    extras = forms.ModelMultipleChoiceField(
        queryset=Extra.objects.filter(active=True),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Booking
        fields = [
            'customer_name','email','phone',
            'start_date','end_date',
            'route_start','route_end','route_notes',
            'purpose','extras'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }