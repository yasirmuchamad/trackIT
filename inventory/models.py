from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Departement(models.Model):
    """Model definition for Departement."""

    # TODO: Define fields here
    name    = models.CharField(max_length=32) 
    leader  = models.CharField(max_length=64)

    class Meta:
        """Meta definition for Departement."""

        verbose_name = 'Departement'
        verbose_name_plural = 'Departements'

    def __str__(self):
        """Unicode representation of Departement."""
        return f"{self.name} {self.leader}"


class Employee(models.Model):
    """Model definition for Employee."""

    # TODO: Define fields here
    user        = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    employee_id = models.CharField(max_length=20, unique=True)
    name        = models.CharField(max_length=100)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    position    = models.CharField(max_length=32)
    email       = models.EmailField(unique=True)
    phone       = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        """Meta definition for Employee."""

        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        """Unicode representation of Employee."""
        return f"{self.employee_id} - {self.name}"

class Category(models.Model):
    """Model definition for Category."""

    # TODO: Define fields here
    name = models.CharField(max_length=32)
     
    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'

    def __str__(self):
        """Unicode representation of Category."""
        return f"{self.name}"

class Item(models.Model):
    """Model definition for Produc_type."""

    # TODO: Define fields here
    sku_code    = models.CharField(max_length=64, unique=True)
    category    = models.ForeignKey(Category, on_delete=models.CASCADE)
    name        = models.CharField(max_length=32)
    brand       = models.CharField(max_length=32, null=True, blank=True)
    model       = models.CharField(max_length=64, null=True, blank=True)
    cpu         = models.CharField(max_length=32, null=True, blank=True)
    ram         = models.CharField(max_length=32, null=True, blank=True)
    storage     = models.CharField(max_length=32, null=True, blank=True)
    display     = models.CharField(max_length=32, null=True, blank=True)
    os          = models.CharField(max_length=32, null=True, blank=True)
    entry_date  = models.DateTimeField(default=timezone.now)

    class Meta:
        """Meta definition for Produc_type."""

        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        """Unicode representation of Produc_type."""
        return f"{self.name} {self.brand} {self.model }"

class Area(models.Model):
    """Model definition for Area."""

    # TODO: Define fields here
    name = models.CharField(max_length=64)
    mainterval = models.PositiveIntegerField(default=6)

    class Meta:
        """Meta definition for Area."""

        verbose_name = 'Area'
        verbose_name_plural = 'Areas'

    def __str__(self):
        """Unicode representation of Area."""
        return f"{self.name} {self.mainterval}"


class Location(models.Model):
    """Model definition for Location."""

    # TODO: Define fields here
    name = models.CharField(max_length=64)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)

    class Meta:
        """Meta definition for Location."""

        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        """Unicode representation of Location."""
        return f"{self.area} {self.name}"


class ItemUnit(models.Model):
    """Model definition for Item."""
    asset_number    = models.CharField(max_length=16, unique=True)
    item            = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='units')
    serial_number   = models.CharField(max_length=64, unique=True, blank=True, null=True)
    location        = models.ForeignKey(Location, on_delete=models.CASCADE)
    ip_address      = models.GenericIPAddressField(null=True, blank=True)
    status          = models.CharField(max_length=20, choices=[
        ('in_warehouse', 'In Warehouse'),
        ('in_use', 'In Use'),
        ('borrowed', 'Borrowed'),
        ('damaged', 'Damaged')
    ])
    condition = models.CharField(max_length=20, choices=[
        ('good', 'Good'),
        ('minor_issue', 'Minor Issue'),
        ('damaged', 'Damaged')
    ])
    current_user    = models.ForeignKey(Employee,on_delete=models.SET_NULL, null=True, blank=True)
    # TODO: Define fields here

    class Meta:
        """Meta definition for Item."""

        verbose_name = 'ItemUnit'
        verbose_name_plural = 'ItemUnits'

    def __str__(self):
        """Unicode representation of Item."""
        return f"{self.asset_number}"

    
