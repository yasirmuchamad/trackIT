from django.contrib import admin
from django.http.request import HttpRequest
from .models import *
from datetime import date

# Register your models here.
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit']

@admin.register(Subdepartment)
class SubdepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'department']

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'grade']

@admin.action(description="Exit employee (Resign)")
def exit_as_resign(modeladmin, request, queryset):
    for employee in queryset:
        employee.is_active = False
        employee.exit_date = date.today()
        employee.exit_type = 'resign'
        employee.save()

        # Tutup history aktif
        EmployeeHistory.objects.filter(
            employee=employee,
            is_active=True
        ).update(
            is_active=False,
            end_date=date.today()
        )

@admin.action(description="Exit employee (Terminated)")
def exit_as_terminated(modeladmin, request, queryset):
    for employee in queryset:
        employee.is_active = False
        employee.exit_date = date.today()
        employee.exit_type = 'terminated'
        employee.save()

        EmployeeHistory.objects.filter(
            employee=employee,
            is_active=True
        ).update(
            is_active=False,
            end_date=date.today()
        )

@admin.action(description="Exit employee (Retired)")
def exit_as_retired(modeladmin, request, queryset):
    for employee in queryset:
        employee.is_active = False
        employee.exit_date = date.today()
        employee.exit_date = 'retired'
        employee.save()

        EmployeeHistory.objects.filter(
            employee=employee,
            is_active=True
        ).update(
            is_active=False,
            end_date=date.today()
        )

# @admin.register(Employee)
# class EmployeeAdmin(admin.ModelAdmin):
#     list_display = ('employee_id', 'name', 'is_active', 'exit_type', 'exit_date')
#     list_filter  = ('is_active', 'exit_type')
#     search_fields= ('employee_id', 'name')
#     action = [
#         exit_as_resign,
#         exit_as_terminated,
#         exit_as_retired,
#     ]

class EmployeeHistoryInline(admin.TabularInline):
    model = EmployeeHistory
    extra = 0
    can_delete = False
    ordering = ('-start_date',)

    readonly_fields = (
        'employee',
        'start_date',
        'end_date',
        'is_active',
    )

    def has_add_permission(self, request, obj=None):
        return False


class EmployeeAddressInline(admin.TabularInline):
    model = EmployeeAddress
    extra = 1

class EmployeeWorkExperienceInline(admin.TabularInline):
    model = EmployeeWorkExperience
    extra = 0
    max_num = 3  # Maksimal 3 pengalaman kerja
    ordering = ('-end_date',)
    
    fields = (
        'company_name',
        'position', 
        'department',
        'start_date',
        'end_date',
        'job_description',
        'reason_for_leaving'
    )
    
    readonly_fields = ('created_at', 'updated_at')

@admin.register(EmployeeWorkExperience)
class EmployeeWorkExperienceAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'company_name',
        'position',
        'start_date',
        'end_date',
        'duration_years'
    )
    
    list_filter = (
        'start_date',
        'end_date',
        'company_name'
    )
    
    search_fields = (
        'employee__name',
        'employee__employee_id',
        'company_name',
        'position'
    )
    
    ordering = ('-end_date', 'employee__name')
    
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('employee', 'company_name', 'position', 'department')
        }),
        ('Periode Kerja', {
            'fields': ('start_date', 'end_date')
        }),
        ('Detail Pekerjaan', {
            'fields': ('job_description', 'reason_for_leaving', 'salary_range'),
            'classes': ('collapse',)
        }),
        ('Referensi', {
            'fields': ('supervisor_name', 'supervisor_contact'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        })
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def duration_years(self, obj):
        """Display work duration in years"""
        return f"{obj.duration_years} tahun"
    duration_years.short_description = 'Durasi'

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'employee_id',
        'name',
        'is_active',
        'employment_status',
        'join_date',
    )
    list_filter = (
        'is_active',
        'employment_status',
    )

    search_fields = (
        'employee_id',
        'name',
    )

    action = [
        exit_as_resign,
        exit_as_terminated,
        exit_as_retired,
    ]

    inlines = [
        EmployeeHistoryInline,
        EmployeeAddressInline,
        EmployeeWorkExperienceInline,
    ]
