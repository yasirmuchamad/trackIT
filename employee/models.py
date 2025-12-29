from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone
import uuid
from datetime import timedelta


# Create your models here.
class Unit(models.Model):
    """Model definition for Unit."""

    # TODO: Define fields here
    name    = models.CharField(max_length=20, choices=[
        ('office', 'Office'),
        ('production', 'Production')
    ])
    class Meta:
        """Meta definition for Unit."""

        verbose_name = 'Unit'
        verbose_name_plural = 'Units'

    def __str__(self):
        """Unicode representation of Unit."""
        return self.name


class Department(models.Model):
    """Model definition for Departement."""

    # TODO: Define fields here
    name    = models.CharField(max_length=20) 
    unit    = models.ForeignKey(Unit, on_delete=models.CASCADE, 
                                related_name='departements')
    class Meta:
        """Meta definition for Departement."""

        verbose_name = 'Departement'
        verbose_name_plural = 'Departements'

    def __str__(self):
        """Unicode representation of Departement."""
        return f"{self.name} - {self.unit.name}"
    
class Subdepartment(models.Model):
    """Model definition for Subdepartement."""

    # TODO: Define fields here
    name        = models.CharField(max_length=64)
    department = models.ForeignKey(Department, 
                                   on_delete=models.CASCADE, 
                                   related_name='subdepartements')
    class Meta:
        """Meta definition for Subdepartement."""

        verbose_name = 'Subdepartement'
        verbose_name_plural = 'Subdepartements'

    def __str__(self):
        """Unicode representation of Subdepartement."""
        return f"{self.name} - {self.department.name}"
    
class Employee(models.Model):
    """Model definition for Employee."""
    EMPLOYMENT_STATUS = [
        ('tetap', 'Tetap'),
        ('probation', 'Probation'),
    ]
    RELIGION = [
        ('islam', 'Islam'),
        ('kristen', 'Kristen'),
        ('katolik', 'Katolik'),
        ('protestan', 'Protestan'),
        ('hindu', 'Hindu'),
        ('budha', 'Budha'),
    ]

    SEX = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    MARITAL_STATUS = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('devorced', 'Devorced'),
        ('widowed',  'Widowed')
    ]

    BLOOD_TYPE = [
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
    ]

    EXIT_TYPE = [
        ('resign', 'Resign'),   #Inisiatif Employee sendiri
        ('terminated', 'Terminated'),   #Diberhentikan
        ('retired', 'Retired')  #Pensiun
    ]

    EXIT_REASON = [
        ('probation_failed', 'Failed Probation'),
        ('performance', 'Performance Issue'),
        ('disciplinary', 'Disciplinary Action'),
        ('company_policy', 'Company Policy'),
        ('absconding', 'Absconding / AWOL'),
        ('personal', 'Personal Reason'),
    ]

    # TODO: Define fields here
    employee_id         = models.PositiveBigIntegerField(unique=True)
    name                = models.CharField(max_length=100)
    join_date           = models.DateField()
    employment_status   = models.CharField(max_length=10,
                                           choices=EMPLOYMENT_STATUS)
    permanent_date      = models.DateField(null=True, 
                                           blank=True,
                                           )
    place_of_birth      = models.CharField(max_length=64,
                                           null=True,
                                           blank=True,
                                           )
    date_of_birth       = models.DateField(null=True,
                                           blank=True,
                                           )

    religion            = models.CharField(max_length=10, 
                                           choices=RELIGION,
                                           null=True,
                                           blank=True,
                                           )
    sex                 = models.CharField(max_length=6,
                                           choices=SEX,
                                           null=True,
                                           blank=True,
                                           )
    marital_status      = models.CharField(max_length=10, 
                                           choices=MARITAL_STATUS,
                                           null=True,
                                           blank=True,
                                           )

    national_id_number  = models.CharField(max_length=16,
                                           null=True,
                                           blank=True, 
                                           validators=[MinLengthValidator(16)]
                                           )
    family_card_number  = models.CharField(max_length=16,
                                           null=True,
                                           blank=True,
                                           validators=[MinLengthValidator(16)]
                                           )
    bpjs_employment     = models.CharField(max_length=16,
                                           null=True,
                                           blank=True,
                                           )
    bpjs_health         = models.CharField(max_length=16,
                                           null=True,
                                           blank=True,
                                           )

    tax_id              = models.CharField(max_length=16, 
                            null=True, 
                            blank=True
                            )

    blood_type          = models.CharField(max_length=3, 
                            choices=BLOOD_TYPE,
                            null=True,
                            blank=True,
                            help_text="Keep empty if unknown"
                            )

    phone               = models.CharField(max_length=16,
                                           null=True,
                                           blank=True
                                           )
    private_mail        = models.EmailField(null=True, blank=True)
    company_mail        = models.EmailField(null=True, blank=True)

    is_active           = models.BooleanField(default=True)
    last_working_date   = models.DateField(null=True, blank=True)
    exit_date           = models.DateField(null=True, 
                            blank=True,
                            help_text="The date employee truely exit"
                            )
    exit_type           = models.CharField(max_length=15,
                            choices=EXIT_TYPE,
                            null=True,
                            blank=True
                            )
    exit_reason         = models.CharField(max_length=100,
                            null=True,
                            blank=True
                            )
    
    class Meta:
        """Meta definition for Employee."""

        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        """Unicode representation of Employee."""
        return f"{self.employee_id} - {self.name}"

    def clean(self):
        super().clean()
        today = timezone.now().date()

        # employee sudah keluar
        if not self.is_active:
            if not self.exit_date:
                raise ValidationError(
                    "Edit date must fill, if employee is not active"
                    )
            if not self.exit_type:
                raise ValidationError(
                    "Edit date must fill, if employee is not active"
                    )
            
        # Employee masih aktif
        if self.is_active:
            if self.exit_date or self.exit_type:
                raise ValidationError(
                    "Employee active can't have exit date."
                )
            
        # Hari terakhir kerja
        if self.last_working_date:
            # tidak boleh dimasa depan
            if self.last_working_date > today:
                raise ValidationError({
                    'last_working_date':'Last working date cannot be in the future.'
                })

            # tidak boleh sebelum tanggal gabung
            if self.join_date and self.last_working_date < self.join_date:
                raise ValidationError({
                    'last_working_date':'Last working date cannot be before join date.'
                })
            
            if not self.exit_date:
                raise ValidationError({
                    'last_working_date':'Exit date must be filled if last working date is set.'
                })
            
            if self.exit_date and self.last_working_date > self.exit_date:
                raise ValidationError({
                    'last_working_date':'Last working date cannot after exit date.'
                })
    
    def get_emergency_contacts(self):
        """Get emergency contacts for this employee"""
        return self.families.filter(is_emergency_contact=True).order_by('emergency_priority', 'name')
    
    def get_primary_emergency_contact(self):
        """Get the primary (highest priority) emergency contact"""
        return self.families.filter(is_emergency_contact=True).order_by('emergency_priority').first()
    
    def has_emergency_contact(self):
        """Check if employee has at least one emergency contact"""
        return self.families.filter(is_emergency_contact=True).exists()
        


class EmployeeAddress(models.Model):
    """Model definition for Employee_address."""
    ADDRESS_TYPE = [
        ('registered', 'Registered Address'),
        ('current', 'Current Address'),
    ]
    # TODO: Define fields here
    employee        = models.ForeignKey(Employee, 
                                        on_delete=models.CASCADE, 
                                        related_name='addresses')
    address_type    = models.CharField(max_length=20, choices=ADDRESS_TYPE)
    address         = models.CharField(max_length=120)
    village         = models.CharField(max_length=32)
    district        = models.CharField(max_length=32)
    city            = models.CharField(max_length=32)
    province        = models.CharField(max_length=32)

    class Meta:
        """Meta definition for Employee_address."""

        verbose_name = 'Employee Address'
        verbose_name_plural = 'Employee Addresses'

    def __str__(self):
        """Unicode representation of Employee_address."""
        return f"{self.employee.name} - {self.address_type} - {self.address}"

class EmployeeFamily(models.Model):
    """Model definition for Employee_family."""
    FAMILY_RELATION = [
        ('child', 'Child'),
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('father_in_law', 'Father-in-law'),
        ('mother_in_law', 'Mother-in-law'),
        ('spouse', 'Spouse'),
        ('sibling', 'Sibling'),
        ('other', 'Other'),
    ]

    SEX = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    # TODO: Define fields here
    employee        = models.ForeignKey(Employee, 
                                        on_delete=models.CASCADE, 
                                        related_name='families')
    name            = models.CharField(max_length=100)
    sex             = models.CharField(max_length=6, 
                                       choices=SEX)
    relationship    = models.CharField(max_length=15, 
                                       choices=FAMILY_RELATION)
    date_of_birth   = models.DateField()
    
    # Emergency contact fields
    phone           = models.CharField(max_length=16, 
                                       blank=True, 
                                       help_text="Phone number for this family member")
    is_emergency_contact = models.BooleanField(
                                       default=False,
                                       help_text="Can this person be contacted in case of emergency?")
    emergency_priority = models.PositiveSmallIntegerField(
                                       default=1,
                                       help_text="Priority order for emergency contact (1=highest priority)")
    
    class Meta:
        """Meta definition for Employee_family."""

        verbose_name = 'Employee Family'
        verbose_name_plural = 'Employee Families'
        ordering = ['emergency_priority', 'relationship', 'name']

    def __str__(self):
        """Unicode representation of Employee_family."""
        emergency_indicator = " (Emergency Contact)" if self.is_emergency_contact else ""
        return f"{self.employee.name} - {self.relationship} - {self.name}{emergency_indicator}"
    
    @classmethod
    def get_emergency_contacts(cls, employee):
        """Get all emergency contacts for an employee, ordered by priority"""
        return cls.objects.filter(
            employee=employee, 
            is_emergency_contact=True
        ).order_by('emergency_priority', 'name')
    
class EmployeeStudied(models.Model):
    """Model definition for Employee_studied."""

    # TODO: Define fields here
    employee            = models.ForeignKey(Employee, 
                                            on_delete=models.CASCADE, 
                                            related_name='educations')
    institution_name    = models.CharField(max_length=100)
    graduation_year     = models.PositiveSmallIntegerField(
                            validators=[MinValueValidator(1900), 
                                        MaxValueValidator(2100)],
                            null=True,
                            blank=True
                        )
    major               = models.CharField(max_length=100, 
                                           null=True, blank=True)
    degree              = models.CharField(max_length=8, 
                                           null=True, blank=True)
    class Meta:
        """Meta definition for Employee_studied."""

        verbose_name = 'Employee Education'
        verbose_name_plural = 'Employee Education Record'

    def __str__(self):
        """Unicode representation of Employee_studied."""
        return f"{self.employee.name} - {self.institution_name}"

class Position(models.Model):
    """Model definition for Position."""

    # TODO: Define fields here
    name    = models.CharField(max_length=64)
    level   = models.CharField(max_length=6, null=True, blank=True)
    grade   = models.CharField(max_length=3, null=True, blank=True)
    class Meta:
        """Meta definition for Position."""

        verbose_name = 'Position'
        verbose_name_plural = 'Positions'

    def __str__(self):
        """Unicode representation of Position."""
        level = f" L{self.level}" if self.level else ""
        grade = f" G{self.grade}" if self.grade else ""
        return f"{self.name}{level}{grade}"


class EmployeeHistory(models.Model):
    """Model definition for Employee_history."""

    # TODO: Define fields here
    employee            = models.ForeignKey(Employee, 
                                            on_delete=models.CASCADE, 
                                            related_name='history')
    subdepartment       = models.ForeignKey(Subdepartment, 
                                            on_delete=models.CASCADE, 
                                            related_name='employee_histories')
    position            = models.ForeignKey(Position, on_delete=models.CASCADE)
    grade               = models.CharField(max_length=3, null=True, blank=True)
    start_date          = models.DateField()
    end_date            = models.DateField(null=True, blank=True)

    is_active           = models.BooleanField(default=True)

    class Meta:
        """Meta definition for Employee_history."""

        verbose_name = 'Employee History'
        verbose_name_plural = 'Employee Histories'
        ordering = ['-start_date']

        #ini bagian prnting
        constraints = [
            models.UniqueConstraint(
                fields=['employee'],
                condition=Q(is_active=True),
                name='unique_active_history_per_employee'
            )
        ]

    def __str__(self):
        """Unicode representation of Employee_history."""
        return f"{self.employee.name} - {self.position.name} - {self.start_date}"

class EmployeeOnboarding(models.Model):
    employee = models.OneToOneField(
        'Employee',
        on_delete=models.CASCADE,
        related_name = 'onboarding'
    )

    token=models.UUIDField(
        default     = uuid.uuid4,
        unique      = True,
        editable    = False
    )

    is_completed    = models.BooleanField(default=False)
    completed_at    = models.DateTimeField(null=True,
                                           blank=True
                                           ) 
    
    expires_at  = models.DateTimeField()
    create_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Employee onboarding'
        verbose_name_plural = 'Employee Onboardings'

    def is_expired(self):
        return timezone.now() > self.expires_at
    
    @classmethod
    def create_for_employee(cls, employee, days_valid=3):
        return cls.objects.create(
            employee=employee,
            expires_at=timezone.now() + timedelta(days_valid)
        )
    
    def __str__(self):
        return f"(self.employee.name) onboarding"


class OnboardingDelivery(models.Model):
    CHANNEL_CHOICES = [
        ("email", "Email"),
        ("whatsapp", "WhatsApp"),
    ]

    onboarding = models.ForeignKey(EmployeeOnboarding,
                                   on_delete=models.CASCADE,
                                   related_name="deliveries"
                                   )
    channel = models.CharField(max_length=10,
                               choices=CHANNEL_CHOICES
                               )
    destination = models.CharField(max_length=255)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.channel} -> {self.destination} "