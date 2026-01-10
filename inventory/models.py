from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class Category(models.Model):
    """Model definition for Category."""

    name = models.CharField(max_length=32)
     
    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """Unicode representation of Category."""
        return f"{self.name}"


class Item(models.Model):
    """Model definition for Item."""
    
    ITEM_TYPES = [
        ('asset', 'Asset'),
        ('non_asset', 'Non-Asset'),
    ]

    sku_code    = models.CharField(max_length=64, unique=True)
    category    = models.ForeignKey(Category, on_delete=models.CASCADE)
    name        = models.CharField(max_length=32)
    item_type   = models.CharField(max_length=20, choices=ITEM_TYPES, default='asset', help_text="Jenis item: Asset atau Non-Asset")
    brand       = models.CharField(max_length=32, null=True, blank=True)
    model       = models.CharField(max_length=64, null=True, blank=True)
    
    # Technical specifications (mainly for assets)
    cpu         = models.CharField(max_length=32, null=True, blank=True, help_text="Untuk item elektronik")
    ram         = models.CharField(max_length=32, null=True, blank=True, help_text="Untuk item elektronik")
    storage     = models.CharField(max_length=32, null=True, blank=True, help_text="Untuk item elektronik")
    display     = models.CharField(max_length=32, null=True, blank=True, help_text="Untuk item elektronik")
    os          = models.CharField(max_length=32, null=True, blank=True, help_text="Untuk item elektronik")
    
    # Non-asset specific fields
    unit_of_measure = models.CharField(max_length=20, null=True, blank=True, help_text="Satuan untuk non-asset (pcs, box, kg, dll)")
    minimum_stock = models.PositiveIntegerField(null=True, blank=True, help_text="Stok minimum untuk non-asset")
    
    entry_date  = models.DateTimeField(default=timezone.now)

    class Meta:
        """Meta definition for Item."""

        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        """Unicode representation of Item."""
        try:
            item_type_display = f"[{self.get_item_type_display()}]"
        except AttributeError:
            # Fallback if item_type field doesn't exist yet
            item_type_display = "[Legacy]"
        
        return f"{item_type_display} {self.name} {self.brand or ''} {self.model or ''}".strip()
    
    @property
    def is_asset(self):
        """Check if item is an asset"""
        try:
            return self.item_type == 'asset'
        except AttributeError:
            # Fallback if item_type field doesn't exist yet
            return True  # Default to asset for legacy items
    
    @property
    def is_non_asset(self):
        """Check if item is a non-asset"""
        try:
            return self.item_type == 'non_asset'
        except AttributeError:
            # Fallback if item_type field doesn't exist yet
            return False


class Area(models.Model):
    """Model definition for Area."""

    name = models.CharField(max_length=64)
    maintenance_interval = models.PositiveIntegerField(
        default=6,
        help_text="Maintenance interval in months"
    )

    class Meta:
        """Meta definition for Area."""

        verbose_name = 'Area'
        verbose_name_plural = 'Areas'

    def __str__(self):
        """Unicode representation of Area."""
        return f"{self.name} (Every {self.maintenance_interval} months)"


class Location(models.Model):
    """Model definition for Location."""

    name = models.CharField(max_length=64)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)

    class Meta:
        """Meta definition for Location."""

        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        """Unicode representation of Location."""
        return f"{self.area.name if self.area else 'No Area'} - {self.name}"


class ItemUnit(models.Model):
    """Model definition for ItemUnit."""
    
    STATUS_CHOICES = [
        ('in_warehouse', 'In Warehouse'),
        ('in_use', 'In Use'),
        ('borrowed', 'Borrowed'),
        ('damaged', 'Damaged'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired')
    ]
    
    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('damaged', 'Damaged')
    ]
    
    asset_number    = models.CharField(max_length=16, unique=True)
    item            = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='units')
    serial_number   = models.CharField(max_length=64, unique=True, blank=True, null=True)
    location        = models.ForeignKey(Location, on_delete=models.CASCADE)
    ip_address      = models.GenericIPAddressField(null=True, blank=True)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_warehouse')
    condition       = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    
    # Relasi ke Employee dari app employee
    current_user    = models.ForeignKey(
        'employee.Employee',
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_items',
        help_text="Employee currently using this item"
    )
    
    # Tracking fields
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    last_maintenance = models.DateField(null=True, blank=True)
    next_maintenance = models.DateField(null=True, blank=True)
    
    # Additional fields
    purchase_date   = models.DateField(null=True, blank=True)
    warranty_expiry = models.DateField(null=True, blank=True)
    notes           = models.TextField(blank=True, help_text="Additional notes about this item")

    class Meta:
        """Meta definition for ItemUnit."""

        verbose_name = 'Item Unit'
        verbose_name_plural = 'Item Units'
        ordering = ['asset_number']

    def __str__(self):
        """Unicode representation of ItemUnit."""
        return f"{self.asset_number} - {self.item.name}"
    
    @property
    def is_available(self):
        """Check if item is available for assignment"""
        return self.status in ['in_warehouse', 'in_use'] and self.condition in ['excellent', 'good', 'fair']
    
    @property
    def needs_maintenance(self):
        """Check if item needs maintenance based on area interval"""
        if not self.last_maintenance or not self.location.area:
            return False
        
        from datetime import timedelta
        interval_days = self.location.area.maintenance_interval * 30  # Convert months to days
        next_maintenance = self.last_maintenance + timedelta(days=interval_days)
        return timezone.now().date() >= next_maintenance
    
    def assign_to_employee(self, employee):
        """Assign this item to an employee"""
        self.current_user = employee
        self.status = 'in_use'
        self.save()
    
    def unassign_from_employee(self):
        """Unassign this item from current employee"""
        self.current_user = None
        self.status = 'in_warehouse'
        self.save()


class Stock(models.Model):
    """Model for tracking non-asset item stock levels."""
    
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='stock', help_text="Non-asset item")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, help_text="Storage location")
    current_stock = models.PositiveIntegerField(default=0, help_text="Current stock quantity")
    reserved_stock = models.PositiveIntegerField(default=0, help_text="Reserved/allocated stock")
    
    # Tracking
    last_updated = models.DateTimeField(auto_now=True)
    last_restocked = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stock Records'
        unique_together = ['item', 'location']
    
    def __str__(self):
        return f"{self.item.name} at {self.location} - Stock: {self.current_stock}"
    
    @property
    def available_stock(self):
        """Available stock (current - reserved)"""
        return max(0, self.current_stock - self.reserved_stock)
    
    @property
    def is_low_stock(self):
        """Check if stock is below minimum level"""
        if self.item.minimum_stock:
            return self.current_stock <= self.item.minimum_stock
        return False
    
    def add_stock(self, quantity, reason="Stock addition"):
        """Add stock quantity"""
        self.current_stock += quantity
        self.last_restocked = timezone.now()
        self.save()
    
    def remove_stock(self, quantity, reason="Stock removal"):
        """Remove stock quantity"""
        if quantity > self.available_stock:
            raise ValueError(f"Insufficient stock. Available: {self.available_stock}, Requested: {quantity}")
        self.current_stock -= quantity
        self.save()
    
    def reserve_stock(self, quantity):
        """Reserve stock for allocation"""
        if quantity > self.available_stock:
            raise ValueError(f"Insufficient stock to reserve. Available: {self.available_stock}, Requested: {quantity}")
        self.reserved_stock += quantity
        self.save()
    
    def release_reserved_stock(self, quantity):
        """Release reserved stock"""
        self.reserved_stock = max(0, self.reserved_stock - quantity)
        self.save()


class Transaction(models.Model):
    """Model definition for Inventory Transaction."""
    
    TRANSACTION_TYPES = [
        ('in', 'Barang Masuk'),
        ('out', 'Barang Keluar'),
        ('transfer', 'Transfer Lokasi'),
        ('maintenance', 'Maintenance'),
        ('return', 'Pengembalian'),
    ]
    
    TRANSACTION_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Basic transaction info
    transaction_number = models.CharField(max_length=20, unique=True, help_text="Auto-generated transaction number")
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    transaction_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, default='pending')
    
    # Item information - support both asset and non-asset items
    item_unit = models.ForeignKey(ItemUnit, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True, help_text="For asset items (trackable units)")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True, help_text="For non-asset items (stock-based)")
    quantity = models.PositiveIntegerField(default=1, help_text="Quantity for this transaction")
    
    # Location information
    from_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions_from')
    to_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions_to')
    
    # Employee information
    from_employee = models.ForeignKey('employee.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions_from')
    to_employee = models.ForeignKey('employee.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions_to')
    
    # Transaction details
    reason = models.CharField(max_length=200, help_text="Reason for transaction")
    notes = models.TextField(blank=True, help_text="Additional notes")
    
    # Approval and tracking
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='requested_transactions')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_transactions')
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """Meta definition for Transaction."""
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-transaction_date']
    
    def __str__(self):
        """Unicode representation of Transaction."""
        if self.item_unit:
            item_name = f"{self.item_unit.item.name} ({self.item_unit.asset_number})"
        elif self.item:
            item_name = f"{self.item.name} (Stock: {self.quantity})"
        else:
            item_name = "Unknown Item"
        return f"{self.transaction_number} - {self.get_transaction_type_display()} - {item_name}"
    
    @property
    def is_asset_transaction(self):
        """Check if this is an asset transaction (ItemUnit-based)"""
        return self.item_unit is not None
    
    @property
    def is_non_asset_transaction(self):
        """Check if this is a non-asset transaction (Item stock-based)"""
        return self.item is not None and self.item_unit is None
    
    @property
    def transaction_item(self):
        """Get the item involved in this transaction"""
        if self.item_unit:
            return self.item_unit.item
        return self.item
    
    def clean(self):
        """Validate transaction data"""
        from django.core.exceptions import ValidationError
        
        # Ensure either item_unit or item is provided, but not both
        if not self.item_unit and not self.item:
            raise ValidationError('Either Item Unit (for assets) or Item (for non-assets) must be specified.')
        
        if self.item_unit and self.item:
            raise ValidationError('Cannot specify both Item Unit and Item. Choose one based on item type.')
        
        # Validate item type consistency
        if self.item_unit and self.item_unit.item.is_non_asset:
            raise ValidationError('Asset transactions cannot use non-asset items. Use Item field instead.')
        
        if self.item and self.item.is_asset:
            raise ValidationError('Non-asset transactions cannot use asset items. Use Item Unit field instead.')
    
    def save(self, *args, **kwargs):
        """Override save to generate transaction number and validate"""
        # Run validation
        self.clean()
        
        if not self.transaction_number:
            # Generate transaction number: TRX-YYYYMMDD-XXXX
            from datetime import datetime
            today = datetime.now()
            date_str = today.strftime('%Y%m%d')
            
            # Get last transaction number for today
            last_transaction = Transaction.objects.filter(
                transaction_number__startswith=f'TRX-{date_str}'
            ).order_by('-transaction_number').first()
            
            if last_transaction:
                last_num = int(last_transaction.transaction_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.transaction_number = f'TRX-{date_str}-{new_num:04d}'
        
        super().save(*args, **kwargs)
    
    def approve(self, approved_by_user):
        """Approve the transaction"""
        self.status = 'approved'
        self.approved_by = approved_by_user
        self.approved_at = timezone.now()
        self.save()
        
        # Execute the transaction logic
        self.execute_transaction()
    
    def execute_transaction(self):
        """Execute the transaction based on type"""
        if self.status != 'approved':
            return
        
        if self.is_asset_transaction:
            # Handle asset transactions (ItemUnit-based)
            item_unit = self.item_unit
            
            if self.transaction_type == 'in':
                # Barang masuk - set to warehouse
                item_unit.status = 'in_warehouse'
                item_unit.location = self.to_location
                item_unit.current_user = None
                
            elif self.transaction_type == 'out':
                # Barang keluar - assign to employee
                item_unit.status = 'in_use'
                item_unit.current_user = self.to_employee
                if self.to_location:
                    item_unit.location = self.to_location
                    
            elif self.transaction_type == 'transfer':
                # Transfer lokasi
                item_unit.location = self.to_location
                
            elif self.transaction_type == 'maintenance':
                # Maintenance
                item_unit.status = 'maintenance'
                item_unit.current_user = None
                
            elif self.transaction_type == 'return':
                # Pengembalian
                item_unit.status = 'in_warehouse'
                item_unit.current_user = None
                item_unit.location = self.to_location
            
            item_unit.save()
            
        elif self.is_non_asset_transaction:
            # Handle non-asset transactions (stock-based)
            from django.db import transaction
            
            with transaction.atomic():
                if self.transaction_type == 'in':
                    # Stock masuk - tambah stok
                    stock, created = Stock.objects.get_or_create(
                        item=self.item,
                        location=self.to_location,
                        defaults={'current_stock': 0}
                    )
                    stock.add_stock(self.quantity, f"Stock in via {self.transaction_number}")
                    
                elif self.transaction_type == 'out':
                    # Stock keluar - kurangi stok
                    try:
                        stock = Stock.objects.get(item=self.item, location=self.from_location or self.to_location)
                        stock.remove_stock(self.quantity, f"Stock out via {self.transaction_number}")
                    except Stock.DoesNotExist:
                        raise ValueError(f"No stock record found for {self.item.name} at specified location")
                    
                elif self.transaction_type == 'transfer':
                    # Transfer stok antar lokasi
                    # Remove from source location
                    from_stock = Stock.objects.get(item=self.item, location=self.from_location)
                    from_stock.remove_stock(self.quantity, f"Transfer out via {self.transaction_number}")
                    
                    # Add to destination location
                    to_stock, created = Stock.objects.get_or_create(
                        item=self.item,
                        location=self.to_location,
                        defaults={'current_stock': 0}
                    )
                    to_stock.add_stock(self.quantity, f"Transfer in via {self.transaction_number}")
        
        # Mark transaction as completed
        self.status = 'completed'
        self.save()