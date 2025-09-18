from django import forms
from .models import MaintenanceSchedule

class MaintenanceUpdateForm(forms.ModelForm):
    """MaintenanceUpdateForm definition."""

    # TODO: Define form fields here
    class Meta:
        model=MaintenanceSchedule
        fields=['performed_date', 'status', 'notes']
        