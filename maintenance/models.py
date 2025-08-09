from django.db import models
from inventory.models import ItemUnit
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta
from datetime import date

class MaintenanceSchedule(models.Model):
    item_unit = models.ForeignKey(ItemUnit, on_delete=models.CASCADE)
    technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    scheduled_date = models.DateField(default=date.today)
    performed_date = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('missed', 'Missed'),
    ], default='scheduled')

    auto_generate_next = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.item_unit} - {self.scheduled_date}"

  