from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from maintenance.models import MaintenanceSchedule
from .forms import MaintenanceUpdateForm

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
    
@login_required    
def update_maintenance(request, pk):
    schedule = get_object_or_404(MaintenanceSchedule, pk=pk, technician=request.user)

    if request.method == 'POST':
        form = MaintenanceUpdateForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('list_recap')
    else:
        form = MaintenanceUpdateForm(instance=schedule)

    return render(request, 'maintenance/update_maintenance.html', {'form':form})