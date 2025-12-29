# Generated manually to fix typo in OnboardingDelivery model

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_onboardingdelivery'),
    ]

    operations = [
        migrations.RenameField(
            model_name='onboardingdelivery',
            old_name='is_succces',
            new_name='is_success',
        ),
    ]