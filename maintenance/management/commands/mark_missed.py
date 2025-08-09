from django.core.management.base import BaseCommand
from maintenance.models import MaintenanceSchedule
from django.utils.timezone import now

class Command(BaseCommand):
    help = "Tandai jadwal yang terlewat sebagai missed"

    def handle(self, *args, **kwargs):
        missed = MaintenanceSchedule.objects.filter(
            scheduled_date__lt=now().date(),
            status='scheduled'
        )
        count = missed.update(status='missed')
        self.stdout.write(self.style.SUCCESS(f"{count} jadwal ditandai sebagai missed"))