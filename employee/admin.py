from django.contrib import admin
from .models import *

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

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'name', 'join_date', 'employment_status']
