from django import forms
from .models import Category, Item, ItemUnit, Transaction
from employee.models import Employee


class CategoryForm(forms.ModelForm):
    """Form definition for Category."""

    class Meta:
        """Meta definition for Category form."""
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'id': 'cat_name', 
            'name': 'cat_name',
            'class': 'form-control', 
            'placeholder': 'Input Category Name'
        })


class ItemForm(forms.ModelForm):
    """Base form definition for Item."""

    class Meta:
        """Meta definition for Item form."""
        model = Item
        exclude = ('entry_date',)

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        
        # Basic Information
        self.fields['sku_code'].widget.attrs.update({
            'id': 'sku_code', 
            'name': 'sku_code',
            'class': 'form-control', 
            'placeholder': 'Example: PC-THTF-E500'
        })
        
        self.fields['category'].widget.attrs.update({
            'id': 'category', 
            'name': 'category',
            'class': 'form-control'
        })
        
        self.fields['name'].widget.attrs.update({
            'id': 'name', 
            'name': 'name',
            'class': 'form-control', 
            'placeholder': 'Input Item Name'
        })
        
        self.fields['item_type'].widget.attrs.update({
            'id': 'item_type', 
            'name': 'item_type',
            'class': 'form-control'
        })
        
        self.fields['brand'].widget.attrs.update({
            'id': 'brand', 
            'name': 'brand',
            'class': 'form-control', 
            'placeholder': 'Input Brand'
        })
        
        self.fields['model'].widget.attrs.update({
            'id': 'model', 
            'name': 'model',
            'class': 'form-control', 
            'placeholder': 'Example: LaserJet Pro'
        })
        
        # Technical Specifications (conditional)
        if 'cpu' in self.fields:
            self.fields['cpu'].widget.attrs.update({
                'id': 'cpu', 
                'name': 'cpu',
                'class': 'form-control', 
                'placeholder': 'Input Processor'
            })
        
        if 'ram' in self.fields:
            self.fields['ram'].widget.attrs.update({
                'id': 'ram', 
                'name': 'ram',
                'class': 'form-control', 
                'placeholder': 'Input Memory Capacity'
            })
        
        if 'storage' in self.fields:
            self.fields['storage'].widget.attrs.update({
                'id': 'storage', 
                'name': 'storage',
                'class': 'form-control', 
                'placeholder': 'Input Storage'
            })
        
        if 'display' in self.fields:
            self.fields['display'].widget.attrs.update({
                'id': 'display', 
                'name': 'display',
                'class': 'form-control', 
                'placeholder': 'Input Display Resolution'
            })
        
        if 'os' in self.fields:
            self.fields['os'].widget.attrs.update({
                'id': 'os', 
                'name': 'os',
                'class': 'form-control', 
                'placeholder': 'Input Operating System'
            })
        
        # Non-asset specific fields (conditional)
        if 'unit_of_measure' in self.fields:
            self.fields['unit_of_measure'].widget.attrs.update({
                'id': 'unit_of_measure', 
                'name': 'unit_of_measure',
                'class': 'form-control', 
                'placeholder': 'pcs, box, kg, liter, dll'
            })
        
        if 'minimum_stock' in self.fields:
            self.fields['minimum_stock'].widget.attrs.update({
                'id': 'minimum_stock', 
                'name': 'minimum_stock',
                'class': 'form-control', 
                'placeholder': 'Minimum stock level',
                'min': '0'
            })


class AssetItemForm(ItemForm):
    """Form for Asset items with technical specifications."""
    
    class Meta:
        model = Item
        fields = [
            'sku_code', 'category', 'name', 'item_type', 'brand', 'model',
            'cpu', 'ram', 'storage', 'display', 'os'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set item_type to asset and hide the field
        self.fields['item_type'].initial = 'asset'
        self.fields['item_type'].widget = forms.HiddenInput()
        
        # Set field labels
        self.fields['sku_code'].label = 'SKU Code'
        self.fields['category'].label = 'Kategori'
        self.fields['name'].label = 'Nama Item'
        self.fields['brand'].label = 'Brand'
        self.fields['model'].label = 'Model'
        self.fields['cpu'].label = 'Processor'
        self.fields['ram'].label = 'Memory (RAM)'
        self.fields['storage'].label = 'Storage'
        self.fields['display'].label = 'Display'
        self.fields['os'].label = 'Operating System'


class NonAssetItemForm(ItemForm):
    """Form for Non-Asset items with inventory management fields."""
    
    class Meta:
        model = Item
        fields = [
            'sku_code', 'category', 'name', 'item_type', 'brand', 'model',
            'unit_of_measure', 'minimum_stock'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set item_type to non_asset and hide the field
        self.fields['item_type'].initial = 'non_asset'
        self.fields['item_type'].widget = forms.HiddenInput()
        
        # Set field labels
        self.fields['sku_code'].label = 'SKU Code'
        self.fields['category'].label = 'Kategori'
        self.fields['name'].label = 'Nama Item'
        self.fields['brand'].label = 'Brand'
        self.fields['model'].label = 'Model'
        self.fields['unit_of_measure'].label = 'Satuan'
        self.fields['minimum_stock'].label = 'Minimum Stock'
        
        # Make unit_of_measure required for non-assets
        self.fields['unit_of_measure'].required = True


class ItemUnitForm(forms.ModelForm):
    """Form definition for ItemUnit."""

    class Meta:
        """Meta definition for ItemUnit form."""
        model = ItemUnit
        exclude = ('created_at', 'updated_at')

    def __init__(self, *args, **kwargs):
        super(ItemUnitForm, self).__init__(*args, **kwargs)
        
        # Basic Information
        self.fields['asset_number'].widget.attrs.update({
            'id': 'asset_number', 
            'name': 'asset_number',
            'class': 'form-control', 
            'placeholder': 'Example: GTI-PC-0001'
        })
        
        self.fields['item'].widget.attrs.update({
            'id': 'item', 
            'name': 'item',
            'class': 'form-control'
        })
        
        self.fields['serial_number'].widget.attrs.update({
            'id': 'serial_number', 
            'name': 'serial_number',
            'class': 'form-control', 
            'placeholder': 'Input serial number'
        })
        
        self.fields['location'].widget.attrs.update({
            'id': 'location', 
            'name': 'location',
            'class': 'form-control'
        })
        
        # Technical Details
        self.fields['ip_address'].widget.attrs.update({
            'id': 'ip_address', 
            'name': 'ip_address',
            'class': 'form-control', 
            'placeholder': 'Example: 192.168.1.100'
        })
        
        # Status & Assignment
        self.fields['status'].widget.attrs.update({
            'id': 'status', 
            'name': 'status',
            'class': 'form-control'
        })
        
        self.fields['condition'].widget.attrs.update({
            'id': 'condition', 
            'name': 'condition',
            'class': 'form-control'
        })
        
        self.fields['current_user'].widget.attrs.update({
            'id': 'current_user', 
            'name': 'current_user',
            'class': 'form-control'
        })
        
        # Maintenance & Warranty
        if 'last_maintenance' in self.fields:
            self.fields['last_maintenance'].widget.attrs.update({
                'id': 'last_maintenance',
                'name': 'last_maintenance', 
                'class': 'form-control',
                'type': 'date'
            })
        
        if 'next_maintenance' in self.fields:
            self.fields['next_maintenance'].widget.attrs.update({
                'id': 'next_maintenance',
                'name': 'next_maintenance',
                'class': 'form-control',
                'type': 'date'
            })
        
        if 'purchase_date' in self.fields:
            self.fields['purchase_date'].widget.attrs.update({
                'id': 'purchase_date',
                'name': 'purchase_date',
                'class': 'form-control',
                'type': 'date'
            })
        
        if 'warranty_expiry' in self.fields:
            self.fields['warranty_expiry'].widget.attrs.update({
                'id': 'warranty_expiry',
                'name': 'warranty_expiry',
                'class': 'form-control',
                'type': 'date'
            })
        
        if 'notes' in self.fields:
            self.fields['notes'].widget.attrs.update({
                'id': 'notes',
                'name': 'notes',
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes about this item'
            })


class TransactionForm(forms.ModelForm):
    """Form definition for Transaction."""

    class Meta:
        """Meta definition for Transaction form."""
        model = Transaction
        fields = [
            'transaction_type', 'item_unit', 'item', 'quantity', 'reason', 'notes',
            'from_location', 'to_location', 'from_employee', 'to_employee'
        ]

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        
        # Transaction Type (only if field exists)
        if 'transaction_type' in self.fields:
            self.fields['transaction_type'].widget.attrs.update({
                'id': 'transaction_type',
                'name': 'transaction_type',
                'class': 'form-control',
                'onchange': 'toggleTransactionFields()'
            })
        
        # Item Unit (for assets)
        if 'item_unit' in self.fields:
            self.fields['item_unit'].widget.attrs.update({
                'id': 'item_unit',
                'name': 'item_unit',
                'class': 'form-control'
            })
            self.fields['item_unit'].required = False
            self.fields['item_unit'].help_text = 'Pilih untuk transaksi barang asset (trackable)'
        
        # Item (for non-assets)
        if 'item' in self.fields:
            self.fields['item'].widget.attrs.update({
                'id': 'item',
                'name': 'item',
                'class': 'form-control'
            })
            self.fields['item'].required = False
            self.fields['item'].help_text = 'Pilih untuk transaksi barang non-asset (consumable)'
            # Filter to show only non-asset items
            try:
                self.fields['item'].queryset = Item.objects.filter(item_type='non_asset')
            except:
                # Fallback if item_type column doesn't exist
                self.fields['item'].queryset = Item.objects.none()
        
        # Quantity
        if 'quantity' in self.fields:
            self.fields['quantity'].widget.attrs.update({
                'id': 'quantity',
                'name': 'quantity',
                'class': 'form-control',
                'min': '1',
                'value': '1'
        })
        
        # Reason
        if 'reason' in self.fields:
            self.fields['reason'].widget.attrs.update({
                'id': 'reason',
                'name': 'reason',
                'class': 'form-control',
                'placeholder': 'Alasan transaksi ini'
            })
        
        # Notes
        if 'notes' in self.fields:
            self.fields['notes'].widget.attrs.update({
                'id': 'notes',
                'name': 'notes',
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Catatan tambahan (opsional)'
            })
        
        # Locations
        if 'from_location' in self.fields:
            self.fields['from_location'].widget.attrs.update({
                'id': 'from_location',
                'name': 'from_location',
                'class': 'form-control'
            })
        
        if 'to_location' in self.fields:
            self.fields['to_location'].widget.attrs.update({
                'id': 'to_location',
                'name': 'to_location',
                'class': 'form-control'
            })
        
        # Employees
        if 'from_employee' in self.fields:
            self.fields['from_employee'].widget.attrs.update({
                'id': 'from_employee',
                'name': 'from_employee',
                'class': 'form-control'
            })
        
        if 'to_employee' in self.fields:
            self.fields['to_employee'].widget.attrs.update({
                'id': 'to_employee',
                'name': 'to_employee',
                'class': 'form-control'
            })
        
        # Set field labels
        if 'transaction_type' in self.fields:
            self.fields['transaction_type'].label = 'Jenis Transaksi'
        if 'item_unit' in self.fields:
            self.fields['item_unit'].label = 'Asset Item (Device/Unit)'
        if 'item' in self.fields:
            self.fields['item'].label = 'Non-Asset Item (Consumable)'
        if 'quantity' in self.fields:
            self.fields['quantity'].label = 'Jumlah'
        if 'reason' in self.fields:
            self.fields['reason'].label = 'Alasan'
        if 'notes' in self.fields:
            self.fields['notes'].label = 'Catatan'
        if 'from_location' in self.fields:
            self.fields['from_location'].label = 'Dari Lokasi'
            self.fields['from_location'].help_text = 'Lokasi asal (untuk transfer/return)'
        if 'to_location' in self.fields:
            self.fields['to_location'].label = 'Ke Lokasi'
            self.fields['to_location'].help_text = 'Lokasi tujuan'
        if 'from_employee' in self.fields:
            self.fields['from_employee'].label = 'Dari Karyawan'
            self.fields['from_employee'].help_text = 'Karyawan yang mengembalikan (untuk return)'
        if 'to_employee' in self.fields:
            self.fields['to_employee'].label = 'Ke Karyawan'
            self.fields['to_employee'].help_text = 'Karyawan yang menerima (untuk barang keluar)'

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        item_unit = cleaned_data.get('item_unit')
        item = cleaned_data.get('item')
        from_location = cleaned_data.get('from_location')
        to_location = cleaned_data.get('to_location')
        from_employee = cleaned_data.get('from_employee')
        to_employee = cleaned_data.get('to_employee')
        
        # Validate that either item_unit or item is provided, but not both
        if not item_unit and not item:
            raise forms.ValidationError('Pilih salah satu: Asset Item (untuk barang trackable) atau Non-Asset Item (untuk consumable).')
        
        if item_unit and item:
            raise forms.ValidationError('Tidak bisa memilih keduanya. Pilih Asset Item ATAU Non-Asset Item.')
        
        # Validation based on transaction type
        if transaction_type == 'in':
            # Barang masuk - harus ada to_location
            if not to_location:
                raise forms.ValidationError('Lokasi tujuan harus diisi untuk barang masuk.')
                
        elif transaction_type == 'out':
            # Barang keluar - untuk asset harus ada to_employee, untuk non-asset bisa tanpa employee
            if item_unit and not to_employee:
                raise forms.ValidationError('Karyawan penerima harus diisi untuk barang asset keluar.')
            # Check if asset item is available
            if item_unit and item_unit.status not in ['in_warehouse']:
                raise forms.ValidationError('Asset item tidak tersedia untuk dipinjamkan.')
                
        elif transaction_type == 'transfer':
            # Transfer - harus ada from_location dan to_location
            if not from_location or not to_location:
                raise forms.ValidationError('Lokasi asal dan tujuan harus diisi untuk transfer.')
            if from_location == to_location:
                raise forms.ValidationError('Lokasi asal dan tujuan tidak boleh sama.')
                
        elif transaction_type == 'return':
            # Return - hanya untuk asset items
            if item:
                raise forms.ValidationError('Pengembalian hanya berlaku untuk asset items, bukan consumable items.')
            if not from_employee:
                raise forms.ValidationError('Karyawan yang mengembalikan harus diisi.')
            if not to_location:
                raise forms.ValidationError('Lokasi pengembalian harus diisi.')
            # Check if item is currently assigned to the employee
            if item_unit and item_unit.current_user != from_employee:
                raise forms.ValidationError('Asset item tidak sedang dipinjam oleh karyawan tersebut.')
        
        return cleaned_data


class TransactionInForm(TransactionForm):
    """Simplified form for Barang Masuk"""
    
    class Meta:
        model = Transaction
        fields = ['item_unit', 'item', 'quantity', 'to_location', 'reason', 'notes']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set transaction type to 'in'
        self.instance.transaction_type = 'in'
        
        # Remove unnecessary fields from display (with safety checks)
        fields_to_remove = ['from_location', 'from_employee', 'to_employee', 'transaction_type']
        for field_name in fields_to_remove:
            if field_name in self.fields:
                del self.fields[field_name]
        
        # Update field requirements for 'in' transactions
        if 'to_location' in self.fields:
            self.fields['to_location'].required = True
            self.fields['to_location'].help_text = 'Lokasi tujuan barang masuk (wajib)'


class TransactionOutForm(TransactionForm):
    """Simplified form for Barang Keluar"""
    
    class Meta:
        model = Transaction
        fields = ['item_unit', 'item', 'quantity', 'to_employee', 'to_location', 'from_location', 'reason', 'notes']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set transaction type to 'out'
        self.instance.transaction_type = 'out'
        
        # Remove unnecessary fields from display (with safety checks)
        fields_to_remove = ['from_employee', 'transaction_type']
        for field_name in fields_to_remove:
            if field_name in self.fields:
                del self.fields[field_name]
        
        # Make to_employee optional for out transactions (required only for assets)
        if 'to_employee' in self.fields:
            self.fields['to_employee'].required = False
            self.fields['to_employee'].help_text = 'Wajib untuk asset items, opsional untuk non-asset'
        
        # Make to_location optional for out transactions
        if 'to_location' in self.fields:
            self.fields['to_location'].required = False
            self.fields['to_location'].help_text = 'Lokasi kerja karyawan (opsional)'
        
        # Add from_location for non-asset stock tracking
        if 'from_location' in self.fields:
            self.fields['from_location'].required = False
            self.fields['from_location'].help_text = 'Lokasi asal stok (untuk non-asset items)'


class TransactionReturnForm(TransactionForm):
    """Simplified form for Pengembalian"""
    
    class Meta:
        model = Transaction
        fields = ['item_unit', 'quantity', 'from_employee', 'to_location', 'reason', 'notes']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set transaction type to 'return'
        self.instance.transaction_type = 'return'
        
        # Remove unnecessary fields from display (with safety checks)
        fields_to_remove = ['to_employee', 'from_location', 'transaction_type', 'item']
        for field_name in fields_to_remove:
            if field_name in self.fields:
                del self.fields[field_name]
        
        # Filter item_unit to only show items currently assigned to employees
        if 'item_unit' in self.fields:
            try:
                self.fields['item_unit'].queryset = ItemUnit.objects.filter(
                    status='in_use',
                    current_user__isnull=False
                ).select_related('item', 'current_user')
                self.fields['item_unit'].help_text = 'Hanya menampilkan asset yang sedang dipinjam'
            except:
                pass