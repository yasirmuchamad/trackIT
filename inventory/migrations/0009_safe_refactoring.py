# Generated manually - Safe refactoring with data cleanup

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


def safe_cleanup_and_prepare(apps, schema_editor):
    """
    Safely clean up data before model changes
    """
    # Clear all current_user references to avoid foreign key conflicts
    with schema_editor.connection.cursor() as cursor:
        # Check if inventory_itemunit table exists and has current_user_id column
        cursor.execute("""
            SELECT COUNT(*) FROM pragma_table_info('inventory_itemunit') 
            WHERE name='current_user_id'
        """)
        
        if cursor.fetchone()[0] > 0:
            # Clear current_user references
            cursor.execute("UPDATE inventory_itemunit SET current_user_id = NULL")
            affected_rows = cursor.rowcount
            print(f"Cleared current_user for {affected_rows} ItemUnit records")


def reverse_cleanup(apps, schema_editor):
    """
    Reverse operation - no-op since we can't restore the references
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0012_employeeworkexperience'),
        ('inventory', '0008_location_area'),
    ]

    operations = [
        # Step 1: Clean up data first
        migrations.RunPython(
            safe_cleanup_and_prepare,
            reverse_cleanup,
        ),
        
        # Step 2: Update Area model - rename mainterval to maintenance_interval
        migrations.RenameField(
            model_name='area',
            old_name='mainterval',
            new_name='maintenance_interval',
        ),
        
        # Step 3: Add help text to Area.maintenance_interval
        migrations.AlterField(
            model_name='area',
            name='maintenance_interval',
            field=models.PositiveIntegerField(default=6, help_text='Maintenance interval in months'),
        ),
        
        # Step 4: Update Category verbose_name_plural
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        
        # Step 5: Add new fields to ItemUnit
        migrations.AddField(
            model_name='itemunit',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itemunit',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='itemunit',
            name='last_maintenance',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='itemunit',
            name='next_maintenance',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='itemunit',
            name='purchase_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='itemunit',
            name='warranty_expiry',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='itemunit',
            name='notes',
            field=models.TextField(blank=True, help_text='Additional notes about this item'),
        ),
        
        # Step 6: Update ItemUnit model options
        migrations.AlterModelOptions(
            name='itemunit',
            options={'ordering': ['asset_number'], 'verbose_name': 'Item Unit', 'verbose_name_plural': 'Item Units'},
        ),
        
        # Step 7: Update ItemUnit status choices
        migrations.AlterField(
            model_name='itemunit',
            name='status',
            field=models.CharField(choices=[('in_warehouse', 'In Warehouse'), ('in_use', 'In Use'), ('borrowed', 'Borrowed'), ('damaged', 'Damaged'), ('maintenance', 'Under Maintenance'), ('retired', 'Retired')], default='in_warehouse', max_length=20),
        ),
        
        # Step 8: Update ItemUnit condition choices
        migrations.AlterField(
            model_name='itemunit',
            name='condition',
            field=models.CharField(choices=[('excellent', 'Excellent'), ('good', 'Good'), ('fair', 'Fair'), ('poor', 'Poor'), ('damaged', 'Damaged')], default='good', max_length=20),
        ),
        
        # Step 9: Remove Employee model (this will automatically handle the foreign key)
        migrations.DeleteModel(
            name='Employee',
        ),
        
        # Step 10: Remove Departement model
        migrations.DeleteModel(
            name='Departement',
        ),
        
        # Step 11: Update ItemUnit.current_user to reference employee.Employee
        migrations.AlterField(
            model_name='itemunit',
            name='current_user',
            field=models.ForeignKey(blank=True, help_text='Employee currently using this item', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_items', to='employee.employee'),
        ),
    ]