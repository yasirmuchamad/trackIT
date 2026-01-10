# Generated migration for Stock model and Transaction updates

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_add_item_type_fields'),
    ]

    operations = [
        # Create Stock model
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_stock', models.PositiveIntegerField(default=0, help_text='Current stock quantity')),
                ('reserved_stock', models.PositiveIntegerField(default=0, help_text='Reserved/allocated stock')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('last_restocked', models.DateTimeField(blank=True, null=True)),
                ('item', models.OneToOneField(help_text='Non-asset item', on_delete=django.db.models.deletion.CASCADE, related_name='stock', to='inventory.item')),
                ('location', models.ForeignKey(help_text='Storage location', on_delete=django.db.models.deletion.CASCADE, to='inventory.location')),
            ],
            options={
                'verbose_name': 'Stock',
                'verbose_name_plural': 'Stock Records',
            },
        ),
        
        # Add unique constraint for Stock
        migrations.AddConstraint(
            model_name='stock',
            constraint=models.UniqueConstraint(fields=('item', 'location'), name='unique_item_location_stock'),
        ),
        
        # Add item field to Transaction (for non-asset transactions)
        migrations.AddField(
            model_name='transaction',
            name='item',
            field=models.ForeignKey(blank=True, help_text='For non-asset items (stock-based)', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='inventory.item'),
        ),
        
        # Make item_unit nullable (since we now support non-asset transactions)
        migrations.AlterField(
            model_name='transaction',
            name='item_unit',
            field=models.ForeignKey(blank=True, help_text='For asset items (trackable units)', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='inventory.itemunit'),
        ),
    ]