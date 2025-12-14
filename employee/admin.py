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