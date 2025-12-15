from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit']

@admin.register(Subdepartement)
class SubdepartementAdmin(admin.ModelAdmin):
    list_display = ['name', 'departement']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'name', 'join_date', 'employment_status']

@admin.register(Employee)
class EmployeeAddressAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'name', 'join_date', 'employment_status']