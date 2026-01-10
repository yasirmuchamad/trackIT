# Generated manually for Item model refactoring

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_add_transaction_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_type',
            field=models.CharField(
                choices=[('asset', 'Asset'), ('non_asset', 'Non-Asset')], 
                default='asset', 
                help_text='Jenis item: Asset atau Non-Asset', 
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='item',
            name='unit_of_measure',
            field=models.CharField(
                blank=True, 
                help_text='Satuan untuk non-asset (pcs, box, kg, dll)', 
                max_length=20, 
                null=True
            ),
        ),
        migrations.AddField(
            model_name='item',
            name='minimum_stock',
            field=models.PositiveIntegerField(
                blank=True, 
                help_text='Stok minimum untuk non-asset', 
                null=True
            ),
        ),
        migrations.AlterField(
            model_name='item',
            name='cpu',
            field=models.CharField(
                blank=True, 
                help_text='Untuk item elektronik', 
                max_length=32, 
                null=True
            ),
        ),
        migrations.AlterField(
            model_name='item',
            name='ram',
            field=models.CharField(
                blank=True, 
                help_text='Untuk item elektronik', 
                max_length=32, 
                null=True
            ),
        ),
        migrations.AlterField(
            model_name='item',
            name='storage',
            field=models.CharField(
                blank=True, 
                help_text='Untuk item elektronik', 
                max_length=32, 
                null=True
            ),
        ),
        migrations.AlterField(
            model_name='item',
            name='display',
            field=models.CharField(
                blank=True, 
                help_text='Untuk item elektronik', 
                max_length=32, 
                null=True
            ),
        ),
        migrations.AlterField(
            model_name='item',
            name='os',
            field=models.CharField(
                blank=True, 
                help_text='Untuk item elektronik', 
                max_length=32, 
                null=True
            ),
        ),
    ]