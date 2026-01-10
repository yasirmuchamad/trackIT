from django.contrib import admin
from .models import Category, Area, Location, Item, ItemUnit


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'maintenance_interval']
    list_editable = ['maintenance_interval']
    search_fields = ['name']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'area']
    list_filter = ['area']
    search_fields = ['name', 'area__name']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['sku_code', 'category', 'name', 'brand', 'model', 'cpu', 'ram', 'storage', 'entry_date']
    list_filter = ['category', 'brand', 'entry_date']
    search_fields = ['sku_code', 'name', 'brand', 'model']
    readonly_fields = ['entry_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('sku_code', 'category', 'name', 'brand', 'model')
        }),
        ('Technical Specifications', {
            'fields': ('cpu', 'ram', 'storage', 'display', 'os'),
            'classes': ('collapse',)
        }),
        ('Tracking', {
            'fields': ('entry_date',)
        })
    )


@admin.register(ItemUnit)
class ItemUnitAdmin(admin.ModelAdmin):
    list_display = [
        'asset_number', 'item', 'serial_number', 'location', 
        'status', 'condition', 'current_user', 'last_maintenance'
    ]
    list_filter = [
        'status', 'condition', 'item__category', 'location__area', 
        'created_at', 'last_maintenance'
    ]
    search_fields = [
        'asset_number', 'serial_number', 'item__name', 
        'current_user__name', 'current_user__employee_id'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('asset_number', 'item', 'serial_number', 'location')
        }),
        ('Status & Assignment', {
            'fields': ('status', 'condition', 'current_user')
        }),
        ('Technical Details', {
            'fields': ('ip_address', 'notes'),
            'classes': ('collapse',)
        }),
        ('Maintenance & Warranty', {
            'fields': ('last_maintenance', 'next_maintenance', 'purchase_date', 'warranty_expiry'),
            'classes': ('collapse',)
        }),
        ('Tracking', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        """Optimize queries with select_related"""
        return super().get_queryset(request).select_related(
            'item', 'item__category', 'location', 'location__area', 'current_user'
        )