from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MaintenanceSchedule
from dateutil.relativedelta import relativedelta

@receiver(post_save, sender=MaintenanceSchedule)
def generate_next_schedule(sender, instance, created, **kwargs):
    if instance.status == 'completed' and instance.auto_generate_next:
        area = getattr(instance.item_unit.location, 'area', None)
        interval = getattr(area, 'maintenance_interval', 6)
        next_date = instance.scheduled_date + relativedelta(months=interval)
        
        exists = MaintenanceSchedule.objects.filter(
            item_unit=instance.item_unit,
            scheduled_date=next_date
        ).exists()

        if not exists:
            MaintenanceSchedule.objects.create(
                item_unit = instance.item_unit,
                scheduled_date=next_date,
                status='scheduled',
                auto_generate_next=True
            )

def notify_technician(sender, instance, created, **kwargs):
    if created and instance.status == 'scheduled':
        print(f"[NOTIFIKASI] Maintenance dijadwalkan untuk {instance.item_unit} pada {instance.scheduled_date}")