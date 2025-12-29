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
    ]
