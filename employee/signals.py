from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


from .models import EmployeeHistory


@receiver(pre_save, sender=EmployeeHistory)
def deactivate_previous_history(sender, instance, **kwargs):
    # when new history save as active,
    # then deactivate previous history active on same employee.

    if not instance.pk and instance.is_active:
        previous_histories = EmployeeHistory.object.filter(
            employee=instance.employee,
            is_active=True
        )

        for history in previous_histories:
            history.is_active = False
            history.end_date = instance.start_date or timezone.now().date()
            history.save(update_fields=['is_active', 'end_date'])