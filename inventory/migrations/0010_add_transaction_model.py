# Generated manually for Transaction model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0012_employeeworkexperience'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0009_safe_refactoring'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_number', models.CharField(help_text='Auto-generated transaction number', max_length=20, unique=True)),
                ('transaction_type', models.CharField(choices=[('in', 'Barang Masuk'), ('out', 'Barang Keluar'), ('transfer', 'Transfer Lokasi'), ('maintenance', 'Maintenance'), ('return', 'Pengembalian')], max_length=20)),
                ('transaction_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('quantity', models.PositiveIntegerField(default=1, help_text='Quantity for this transaction')),
                ('reason', models.CharField(help_text='Reason for transaction', max_length=200)),
                ('notes', models.TextField(blank=True, help_text='Additional notes')),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_transactions', to=settings.AUTH_USER_MODEL)),
                ('from_employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions_from', to='employee.employee')),
                ('from_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions_from', to='inventory.location')),
                ('item_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='inventory.itemunit')),
                ('requested_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requested_transactions', to=settings.AUTH_USER_MODEL)),
                ('to_employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions_to', to='employee.employee')),
                ('to_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions_to', to='inventory.location')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'ordering': ['-transaction_date'],
            },
        ),
    ]