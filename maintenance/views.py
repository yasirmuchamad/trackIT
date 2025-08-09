from django.shortcuts import render
from django.views.generic import ListView

from maintenance.models import MaintenanceSchedule

class MaintenanceRecapView(ListView):
    model = MaintenanceSchedule
    template_name = 'maintenance/recap.html'
    context_object_name = 'schedules'

    def get_queryset(self):
        queryset =  MaintenanceSchedule.objects.all().order_by('-scheduled_date')
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset
    
def update_maintenance(request, pk):
    