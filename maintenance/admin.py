from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(MaintenanceSchedule)
class MaintenanceScheduleAdmin(admin.ModelAdmin):
    list_display = ['item_unit','technician', 'scheduled_date', 'performed_date', 'status', 'auto_generate_next', 'notes']