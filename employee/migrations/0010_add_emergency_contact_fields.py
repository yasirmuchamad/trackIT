# Generated manually to add emergency contact fields to EmployeeFamily

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0009_fix_onboarding_delivery_typo'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeefamily',
            name='phone',
            field=models.CharField(blank=True, help_text='Phone number for this family member', max_length=16),
        ),
        migrations.AddField(
            model_name='employeefamily',
            name='is_emergency_contact',
            field=models.BooleanField(default=False, help_text='Can this person be contacted in case of emergency?'),
        ),
        migrations.AddField(
            model_name='employeefamily',
            name='emergency_priority',
            field=models.PositiveSmallIntegerField(default=1, help_text='Priority order for emergency contact (1=highest priority)'),
        ),
        migrations.AlterField(
            model_name='employeefamily',
            name='relationship',
            field=models.CharField(choices=[('child', 'Child'), ('father', 'Father'), ('mother', 'Mother'), ('father_in_law', 'Father-in-law'), ('mother_in_law', 'Mother-in-law'), ('spouse', 'Spouse'), ('sibling', 'Sibling'), ('other', 'Other')], max_length=15),
        ),
        migrations.AlterModelOptions(
            name='employeefamily',
            options={'ordering': ['emergency_priority', 'relationship', 'name'], 'verbose_name': 'Employee Family', 'verbose_name_plural': 'Employee Families'},
        ),
    ]