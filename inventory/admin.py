from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ['name', 'leader']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'name', 'departement', 'position', 'email', 'phone']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display =  ['sku_code', 'category', 'name', 'brand', 'model', 'cpu', 'ram', 'storage', 'display', 'os','entry_date']

@admin.register(ItemUnit)
class ItemUnitAdmin(admin.ModelAdmin):
    list_display =  ['item', 'serial_number', 'location', 'ip_address', 'status', 'condition', 'current_user']