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
                    results = send_onboarding_links(
                        onboarding,
                        email=employee.private_mail,
                        phone=employee.phone,
                    )
                    
                    # Check results and show appropriate messages
                    success_messages = []
                    error_messages = []
                    
                    if employee.private_mail:
                        if results['email']:
                            success_messages.append(f"onboarding email sent to {employee.private_mail}")
                        else:
                            error_messages.append(f"failed to send email to {employee.private_mail}")
                    
                    if employee.phone:
                        if results['whatsapp']:
                            success_messages.append(f"onboarding WhatsApp sent to {employee.phone}")
                        else:
                            error_messages.append(f"failed to send WhatsApp to {employee.phone}")
                    
                    if success_messages:
                        messages.success(
                            request,
                            f"Employee {employee.name} created successfully. " + 
                            " and ".join(success_messages).capitalize() + "."
                        )
                    
                    if error_messages:
                        messages.warning(
                            request,
                            "Employee created but some notifications failed: " + 
                            ", ".join(error_messages) + "."
                        )
                    
                    if not success_messages and not error_messages:
                        messages.success(
                            request,
                            f"Employee {employee.name} created successfully."
                        )
                        
                except Exception as e:
                    messages.warning(
                        request,
                        f"Employee {employee.name} created but failed to send onboarding notifications: {str(e)}"
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
        
        # Deactivate current history (if exists)
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
        
        action_message = "Position changed" if current_history else "First position assigned"
        messages.success(request, f"{action_message} for {employee.name}")
        return redirect("employees:employee_detail", employee_id=employee.employee_id)
    
    # Get all units with their departments and subdepartments
    units = Unit.objects.all()
    current_history = employee.history.filter(is_active=True).first()
    
    context = {
        'employee': employee,
        'current_history': current_history,
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
    
    # Employees without position
    employees_without_position = Employee.objects.filter(
        is_active=True,
        history__isnull=True
    ).count()
    
    context = {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'inactive_employees': inactive_employees,
        'recent_employees': recent_employees,
        'employees_without_position': employees_without_position,
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
            results = send_onboarding_links(
                onboarding,
                email=onboarding.employee.private_mail,
                phone=onboarding.employee.phone,
            )
            
            # Check results and show appropriate messages
            success_messages = []
            error_messages = []
            
            if onboarding.employee.private_mail:
                if results['email']:
                    success_messages.append(f"email sent to {onboarding.employee.private_mail}")
                else:
                    error_messages.append(f"failed to send email to {onboarding.employee.private_mail}")
            
            if onboarding.employee.phone:
                if results['whatsapp']:
                    success_messages.append(f"WhatsApp sent to {onboarding.employee.phone}")
                else:
                    error_messages.append(f"failed to send WhatsApp to {onboarding.employee.phone}")
            
            if success_messages:
                messages.success(
                    request, 
                    f"Onboarding notifications resent to {onboarding.employee.name}: " + 
                    ", ".join(success_messages) + "."
                )
            
            if error_messages:
                messages.error(
                    request, 
                    f"Failed to resend some notifications to {onboarding.employee.name}: " + 
                    ", ".join(error_messages) + "."
                )
            
            if not success_messages and not error_messages:
                messages.warning(
                    request, 
                    f"No contact information available for {onboarding.employee.name}."
                )
                
        except Exception as e:
            messages.error(request, f"Failed to resend onboarding notifications: {str(e)}")
    
    return redirect("employees:onboarding_list")


# Onboarding Form Views (Public - No login required)
def onboarding_form(request, token):
    """Public onboarding form for employees to complete their data"""
    try:
        onboarding = get_object_or_404(EmployeeOnboarding, token=token)
        
        # Check if onboarding is expired
        if onboarding.is_expired():
            return render(request, 'employee/onboarding_expired.html', {
                'onboarding': onboarding
            })
        
        # Check if already completed
        if onboarding.is_completed:
            return render(request, 'employee/onboarding_completed.html', {
                'onboarding': onboarding
            })
        
        employee = onboarding.employee
        
        if request.method == 'POST':
            # Process form submission
            return process_onboarding_form(request, onboarding)
        
        # Show onboarding form
        context = {
            'onboarding': onboarding,
            'employee': employee,
        }
        
        return render(request, 'employee/onboarding_form.html', context)
        
    except Exception as e:
        return render(request, 'employee/onboarding_error.html', {
            'error': str(e)
        })


def process_onboarding_form(request, onboarding):
    """Process onboarding form submission"""
    from django.utils import timezone
    from datetime import datetime
    
    employee = onboarding.employee
    
    try:
        # Update employee basic data
        employee.place_of_birth = request.POST.get('place_of_birth', employee.place_of_birth)
        employee.date_of_birth = request.POST.get('date_of_birth') or employee.date_of_birth
        employee.religion = request.POST.get('religion', employee.religion)
        employee.sex = request.POST.get('sex', employee.sex)
        employee.marital_status = request.POST.get('marital_status', employee.marital_status)
        employee.national_id_number = request.POST.get('national_id_number', employee.national_id_number)
        employee.family_card_number = request.POST.get('family_card_number', employee.family_card_number)
        employee.blood_type = request.POST.get('blood_type', employee.blood_type)
        employee.phone = request.POST.get('phone', employee.phone)
        
        # Update BPJS and Tax information
        employee.bpjs_employment = request.POST.get('bpjs_employment', employee.bpjs_employment)
        employee.bpjs_health = request.POST.get('bpjs_health', employee.bpjs_health)
        employee.tax_id = request.POST.get('tax_id', employee.tax_id)
        
        # Validate required fields
        errors = []
        if not employee.place_of_birth:
            errors.append("Place of birth is required")
        if not employee.date_of_birth:
            errors.append("Date of birth is required")
        if not employee.sex:
            errors.append("Gender is required")
        if not employee.phone:
            errors.append("Phone number is required")
        
        if errors:
            context = {
                'onboarding': onboarding,
                'employee': employee,
                'errors': errors,
            }
            return render(request, 'employee/onboarding_form.html', context)
        
        # Save employee data
        employee.save()
        
        # Process Address Information
        process_address_data(request, employee)
        
        # Process Family Information
        process_family_data(request, employee)
        
        # Process Education Information
        process_education_data(request, employee)
        
        # Mark onboarding as completed
        onboarding.is_completed = True
        onboarding.completed_at = timezone.now()
        onboarding.save()
        
        return render(request, 'employee/onboarding_success.html', {
            'onboarding': onboarding,
            'employee': employee
        })
        
    except Exception as e:
        context = {
            'onboarding': onboarding,
            'employee': employee,
            'errors': [f"Error saving data: {str(e)}"],
        }
        return render(request, 'employee/onboarding_form.html', context)


def process_address_data(request, employee):
    """Process address information from onboarding form"""
    from employee.models import EmployeeAddress
    
    # Current Address
    current_address = request.POST.get('current_address')
    current_village = request.POST.get('current_village')
    current_district = request.POST.get('current_district')
    current_city = request.POST.get('current_city')
    current_province = request.POST.get('current_province')
    
    if current_address and current_village and current_district and current_city and current_province:
        # Delete existing current address
        EmployeeAddress.objects.filter(employee=employee, address_type='current').delete()
        
        # Create new current address
        EmployeeAddress.objects.create(
            employee=employee,
            address_type='current',
            address=current_address,
            village=current_village,
            district=current_district,
            city=current_city,
            province=current_province
        )
    
    # Registered Address (if different)
    same_address = request.POST.get('same_address') == 'on'
    
    if not same_address:
        registered_address = request.POST.get('registered_address')
        registered_village = request.POST.get('registered_village')
        registered_district = request.POST.get('registered_district')
        registered_city = request.POST.get('registered_city')
        registered_province = request.POST.get('registered_province')
        
        if registered_address and registered_village and registered_district and registered_city and registered_province:
            # Delete existing registered address
            EmployeeAddress.objects.filter(employee=employee, address_type='registered').delete()
            
            # Create new registered address
            EmployeeAddress.objects.create(
                employee=employee,
                address_type='registered',
                address=registered_address,
                village=registered_village,
                district=registered_district,
                city=registered_city,
                province=registered_province
            )
    else:
        # Copy current address to registered address
        if current_address:
            EmployeeAddress.objects.filter(employee=employee, address_type='registered').delete()
            EmployeeAddress.objects.create(
                employee=employee,
                address_type='registered',
                address=current_address,
                village=current_village,
                district=current_district,
                city=current_city,
                province=current_province
            )


def process_family_data(request, employee):
    """Process family information from onboarding form"""
    from employee.models import EmployeeFamily
    from datetime import datetime
    
    # Delete existing family data
    EmployeeFamily.objects.filter(employee=employee).delete()
    
    # Process multiple family members
    family_count = int(request.POST.get('family_count', 0))
    
    for i in range(family_count):
        name = request.POST.get(f'family_name_{i}')
        sex = request.POST.get(f'family_sex_{i}')
        relationship = request.POST.get(f'family_relationship_{i}')
        date_of_birth = request.POST.get(f'family_dob_{i}')
        phone = request.POST.get(f'family_phone_{i}', '')
        is_emergency = request.POST.get(f'family_emergency_{i}') == 'on'
        emergency_priority = request.POST.get(f'family_priority_{i}', 1)
        
        if name and sex and relationship and date_of_birth:
            try:
                # Convert date string to date object
                dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
                
                EmployeeFamily.objects.create(
                    employee=employee,
                    name=name,
                    sex=sex,
                    relationship=relationship,
                    date_of_birth=dob,
                    phone=phone,
                    is_emergency_contact=is_emergency,
                    emergency_priority=int(emergency_priority) if emergency_priority else 1
                )
            except ValueError:
                # Skip invalid dates
                continue


def process_education_data(request, employee):
    """Process education information from onboarding form"""
    from employee.models import EmployeeStudied
    
    # Delete existing education data
    EmployeeStudied.objects.filter(employee=employee).delete()
    
    # Process multiple education records
    education_count = int(request.POST.get('education_count', 0))
    
    for i in range(education_count):
        institution = request.POST.get(f'education_institution_{i}')
        graduation_year = request.POST.get(f'education_year_{i}')
        major = request.POST.get(f'education_major_{i}')
        degree = request.POST.get(f'education_degree_{i}')
        
        if institution:
            EmployeeStudied.objects.create(
                employee=employee,
                institution_name=institution,
                graduation_year=int(graduation_year) if graduation_year else None,
                major=major or '',
                degree=degree or ''
            )
