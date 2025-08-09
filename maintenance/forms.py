from django import forms
from .models import MaintenanceSchedule

class MaintenanceUpdateForm(forms.Form):
    """MaintenanceUpdateForm definition."""

    # TODO: Define form fields here
    class Meta:
        models=MaintenanceSchedule
        fields=['performed_date', 'status', 'notes']
        