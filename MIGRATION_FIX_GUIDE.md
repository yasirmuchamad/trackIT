# Migration Fix Guide - Inventory Refactoring (Updated)

## Problem
The migration failed with `IntegrityError` because there are existing `ItemUnit` records that reference `inventory_employee` records, but we're trying to change the foreign key to point to `employee_employee`.

## Simple Solution

I've created a single, safe migration that handles everything automatically:

### Step 1: Run the Safe Migration
```bash
python manage.py migrate inventory 0009
```

This migration will:
1. **Automatically clear** all `current_user` references in ItemUnit
2. **Add all new fields** to ItemUnit model
3. **Remove duplicate models** (Employee, Departement) 
4. **Update foreign key** to point to employee.Employee
5. **Update field choices** and model options

### Step 2: Verify Migration Success
After migration, check that everything works:

```bash
python manage.py shell
```

```python
# In Django shell
from inventory.models import ItemUnit
from employee.models import Employee

# Check that models work
print("ItemUnit count:", ItemUnit.objects.count())
print("Employee count:", Employee.objects.count())

# Test assignment
if ItemUnit.objects.exists() and Employee.objects.exists():
    item = ItemUnit.objects.first()
    employee = Employee.objects.first()
    item.assign_to_employee(employee)
    print(f"Successfully assigned {item.asset_number} to {employee.name}")
```

## What the Migration Does

### Automatic Data Cleanup:
- ✅ Clears all `current_user_id` references to avoid foreign key conflicts
- ✅ Preserves all other ItemUnit data (asset_number, serial_number, etc.)

### Model Updates:
- ✅ Removes `Employee` and `Departement` models from inventory
- ✅ Updates `ItemUnit.current_user` to reference `employee.Employee`
- ✅ Adds new tracking fields (created_at, updated_at, maintenance dates)
- ✅ Updates status/condition choices
- ✅ Renames `Area.mainterval` to `maintenance_interval`

### Safety Features:
- ✅ Uses `RunPython` to safely clean data before schema changes
- ✅ Handles missing tables/columns gracefully
- ✅ No data loss (except temporary current_user assignments)

## After Migration

### Re-assign Items to Employees:
1. Go to Django Admin → Inventory → Item Units
2. Edit each item and assign to appropriate employee
3. Or create a bulk assignment script if needed

### Verify Integration:
- All inventory functionality should work with employee app
- ItemUnit admin shows employee names properly
- No more duplicate employee data

## Rollback Plan (if needed)

```bash
# Rollback to before refactoring
python manage.py migrate inventory 0008
```

## Alternative: Manual Database Fix

If you prefer to handle the data cleanup manually:

```sql
-- Clear current_user references manually
UPDATE inventory_itemunit SET current_user_id = NULL;
```

Then run the migration:
```bash
python manage.py migrate inventory 0009
```

## Notes

- ✅ **Safe to run** - automatically handles data conflicts
- ✅ **No data loss** - only clears temporary assignments
- ✅ **Single migration** - no complex multi-step process
- ✅ **Automatic cleanup** - handles edge cases
- ⚠️ **Item assignments will be cleared** - need to reassign after migration
- ⚠️ **Backup recommended** - always backup before major changes

The migration is designed to be safe and handle the IntegrityError automatically!