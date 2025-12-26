from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from employee.forms import EmployeeCreateForm, EmployeeUpdateForm, EmployeeSearchForm
from employee.models import (
    Employee, EmployeeOnboarding, EmployeeHistory, 
    EmployeeAddress, EmployeeFamily, EmployeeStudied,
    Unit, Department, Subdepartment, Position
)
from employee.services.onboarding_delivery import send_onboarding_links


# Employee CRUD Views
@login_required
def employee_list(request):
    """List all employees with search and pagination"""
    employees = Employee.objects.select_related().order_by('-employee_id')
    
    # Search functionality
    search_form = EmployeeSearchForm(request.GET)
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search')
        status_filter = search_form.cleaned_data.get('status')
        unit_filter = search_form.cleaned_data.get('unit')
        
        if search_query:
            employees = employees.filter(
                Q(name__icontains=search_query) |
                Q(employee_id__icontains=search_query) |
                Q(company_mail__icontains=search_query)
            )
        
        if status_filter:
            if status_filter == 'active':
                employees = employees.filter(is_active=True)
            elif status_filter == 'inactive':
                employees = employees.filter(is_active=False)
        
        if unit_filter:
            employees = employees.filter(
                history__subdepartment__department__unit=unit_filter,
                history__is_active=True
            )
    
    # Pagination
    paginator = Paginator(employees, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'total_employees': employees.count()
    }
    
    return render(request, 'employee/list.html', context)


@login_required
def employee_detail(request, employee_id):
    """Detail view for a specific employee"""
    employee = get_object_or_404(Employee, employee_id=employee_id)
    
    # Get current position
    current_history = employee.history.filter(is_active=True).first()
    
    # Get all history
    history = employee.history.all()
    
    # Get addresses
    addresses = employee.addresses.all()
    
    # Get family members
    families = employee.families.all()
    
    # Get education records
    educations = employee.educations.all()
    
    context = {
        'employee': employee,
        'current_history': current_history,
        'history': history,
        'addresses': addresses,
        'families': families,
        'educations': educations,
    }
    
    return render(request, 'employee/detail.html', context)


@login_required
def create_employee(request):
    """Create new employee"""
    if request.method == "POST":
        form = EmployeeCreateForm(request.POST)

        if form.is_valid():
            employee = form.save()

            # Create onboarding if email or phone provided
            if employee.private_mail or employee.phone:
                onboarding = EmployeeOnboarding.create_for_employee(employee)
                
                try:
                    send_onboarding_links(
                        onboarding,
                        email=employee.private_mail,
                        phone=employee.phone,
                    )
                    messages.success(
                        request,
                        f"Employee {employee.name} created and onboarding link sent."
                    )
                except Exception as e:
                    messages.warning(
                        request,
                        f"Employee {employee.name} created but failed to send onboarding link: {str(e)}"
                    )
            else:
                messages.success(
                    request,
                    f"Employee {employee.name} created successfully."
                )
            
            return redirect("employees:employee_detail", employee_id=employee.employee_id)
        
    else:
        form = EmployeeCreateForm()

    return render(
        request,
        "employee/create.html",
        {"form": form}
    )


@login_required
def update_employee(request, employee_id):
    """Update employee information"""
    employee = get_object_or_404(Employee, employee_id=employee_id)
    
    if request.method == "POST":
        form = EmployeeUpdateForm(request.POST, instance=employee)
        
        if form.is_valid():
            form.save()
            messages.success(request, f"Employee {employee.name} updated successfully.")
            return redirect("employees:employee_detail", employee_id=employee.employee_id)
    else:
        form = EmployeeUpdateForm(instance=employee)
    
    context = {
        'form': form,
        'employee': employee
    }
    
    return render(request, 'employee/update.html', context)


@login_required
def deactivate_employee(request, employee_id):
    """Deactivate employee (soft delete)"""
    employee = get_object_or_404(Employee, employee_id=employee_id)
    
    if request.method == "POST":
        exit_type = request.POST.get('exit_type')
        exit_reason = request.POST.get('exit_reason')
        last_working_date = request.POST.get('last_working_date')
        exit_date = request.POST.get('exit_date')
        
        employee.is_active = False
        employee.exit_type = exit_type
        employee.exit_reason = exit_reason
        if last_working_date:
            employee.last_working_date = last_working_date
        if exit_date:
            employee.exit_date = exit_date
        
        try:
            employee.save()
            
            # Deactivate current position
            current_history = employee.history.filter(is_active=True).first()
            if current_history:
                current_history.is_active = False
                current_history.end_date = last_working_date or exit_date
                current_history.save()
            
            messages.success(request, f"Employee {employee.name} has been deactivated.")
            return redirect("employees:employee_detail", employee_id=employee.employee_id)
        except Exception as e:
            messages.error(request, f"Error deactivating employee: {str(e)}")
    
    context = {
        'employee': employee,
        'exit_types': Employee.EXIT_TYPE,
        'exit_reasons': Employee.EXIT_REASON
    }
    
    return render(request, 'employee/deactivate.html', context)


@login_required
def employee_history_create(request, employee_id):
    """Create new position history for employee"""
    employee = get_object_or_404(Employee, employee_id=employee_id)
    
    if request.method == "POST":
        subdepartment_id = request.POST.get('subdepartment')
        position_id = request.POST.get('position')
        grade = request.POST.get('grade')
        start_date = request.POST.get('start_date')
        
        # Deactivate current history
        current_history = employee.history.filter(is_active=True).first()
        if current_history:
            current_history.is_active = False
            current_history.end_date = start_date
            current_history.save()
        
        # Create new history
        EmployeeHistory.objects.create(
            employee=employee,
            subdepartment_id=subdepartment_id,
            position_id=position_id,
            grade=grade,
            start_date=start_date,
            is_active=True
        )
        
        messages.success(request, f"New position history added for {employee.name}")
        return redirect("employees:employee_detail", employee_id=employee.employee_id)
    
    # Get all units with their departments and subdepartments
    units = Unit.objects.all()
    
    context = {
        'employee': employee,
        'subdepartments': Subdepartment.objects.select_related('department__unit').all(),
        'positions': Position.objects.all(),
        'units': units
    }
    
    return render(request, 'employee/history_create.html', context)


# Dashboard and Statistics
@login_required
def employee_dashboard(request):
    """Employee dashboard with statistics"""
    total_employees = Employee.objects.count()
    active_employees = Employee.objects.filter(is_active=True).count()
    inactive_employees = Employee.objects.filter(is_active=False).count()
    
    # Recent employees (last 30 days)
    from datetime import datetime, timedelta
    thirty_days_ago = datetime.now().date() - timedelta(days=30)
    recent_employees = Employee.objects.filter(join_date__gte=thirty_days_ago).count()
    
    # Employees by unit
    units_stats = []
    for unit in Unit.objects.all():
        unit_count = Employee.objects.filter(
            history__subdepartment__department__unit=unit,
            history__is_active=True,
            is_active=True
        ).distinct().count()
        units_stats.append({
            'unit': unit,
            'count': unit_count
        })
    
    # Employees by employment status
    probation_count = Employee.objects.filter(
        employment_status='probation',
        is_active=True
    ).count()
    
    permanent_count = Employee.objects.filter(
        employment_status='tetap',
        is_active=True
    ).count()
    
    context = {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'inactive_employees': inactive_employees,
        'recent_employees': recent_employees,
        'units_stats': units_stats,
        'probation_count': probation_count,
        'permanent_count': permanent_count,
    }
    
    return render(request, 'employee/dashboard.html', context)


# AJAX Views
@login_required
@require_http_methods(["GET"])
def get_departments(request):
    """AJAX view to get departments by unit"""
    unit_id = request.GET.get('unit_id')
    departments = Department.objects.filter(unit_id=unit_id).values('id', 'name')
    return JsonResponse({'departments': list(departments)})


@login_required
@require_http_methods(["GET"])
def get_subdepartments(request):
    """AJAX view to get subdepartments by department"""
    department_id = request.GET.get('department_id')
    subdepartments = Subdepartment.objects.filter(department_id=department_id).values('id', 'name')
    return JsonResponse({'subdepartments': list(subdepartments)})


# Onboarding Views
@login_required
def onboarding_list(request):
    """List all onboarding records"""
    onboardings = EmployeeOnboarding.objects.select_related('employee').order_by('-create_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter == 'completed':
        onboardings = onboardings.filter(is_completed=True)
    elif status_filter == 'pending':
        onboardings = onboardings.filter(is_completed=False)
    elif status_filter == 'expired':
        from django.utils import timezone
        onboardings = onboardings.filter(
            expires_at__lt=timezone.now(),
            is_completed=False
        )
    
    # Pagination
    paginator = Paginator(onboardings, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter
    }
    
    return render(request, 'employee/onboarding_list.html', context)


@login_required
def resend_onboarding(request, onboarding_id):
    """Resend onboarding link"""
    onboarding = get_object_or_404(EmployeeOnboarding, id=onboarding_id)
    
    if request.method == "POST":
        try:
            send_onboarding_links(
                onboarding,
                email=onboarding.employee.private_mail,
                phone=onboarding.employee.phone,
            )
            messages.success(request, f"Onboarding link resent to {onboarding.employee.name}")
        except Exception as e:
            messages.error(request, f"Failed to resend onboarding link: {str(e)}")
    
    return redirect("employees:onboarding_list")
