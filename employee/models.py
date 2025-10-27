from django.db import models

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
        return f"{self.name}"


class Departement(models.Model):
    """Model definition for Departement."""

    # TODO: Define fields here
    name    = models.CharField(max_length=20) 
    unit    = models.ForeignKey(Unit, on_delete=models.CASCADE)
    class Meta:
        """Meta definition for Departement."""

        verbose_name = 'Departement'
        verbose_name_plural = 'Departements'

    def __str__(self):
        """Unicode representation of Departement."""
        return f"{self.name}{self.unit}"
    
class Subdepartement(models.Model):
    """Model definition for Subdepartement."""

    # TODO: Define fields here
    name        = models.CharField(max_length=64)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    class Meta:
        """Meta definition for Subdepartement."""

        verbose_name = 'Subdepartement'
        verbose_name_plural = 'Subdepartements'

    def __str__(self):
        """Unicode representation of Subdepartement."""
        return f"{self.models}{self.departement}"
    
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
    # TODO: Define fields here
    employee_id         = models.PositiveBigIntegerField()
    name                = models.CharField(max_length=100)
    join_date           = models.DateField()
    employment_status   = models.CharField(max_length=10, choices=EMPLOYMENT_STATUS)
    permanent_date      = models.DateField()
    place_of_birth      = models.CharField(max_length=64)
    date_of_birth       = models.DateField()
    religion            = models.CharField(max_length=10, choices=RELIGION)
    sex                 = models.CharField(max_length=6, choices=SEX)
    marital_status      = models.CharField(max_length=10, choices=MARITAL_STATUS)
    national_id_number  = models.CharField(max_length=16)
    family_card_number  = models.CharField(max_length=16)
    bpjs_employment     = models.CharField(max_length=16)
    bpjs_healt          = models.CharField(max_length=16)
    tax_id              = models.CharField(max_length=16, null=True, blank=True)
    blood_type          = models.CharField(max_length=3, choices=BLOOD_TYPE)
    phone               = models.CharField(max_length=16)
    private_mail        = models.EmailField(null=True, blank=True)
    company_mail        = models.EmailField(null=True, blank=True)
    
    class Meta:
        """Meta definition for Employee."""

        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        """Unicode representation of Employee."""
        return f"{self.employee_id}-{self.name}-{self.employment_status}-{self.sex}-{self.blood_type}-{self.phone}-{self.private_mail}"


class Employee_address(models.Model):
    """Model definition for Employee_address."""
    ADDRESS_TYPE = [
        ('registered_address', 'Registered_address'),
        ('current_address', 'Current_address'),
    ]
    # TODO: Define fields here
    employee        = models.ForeignKey(Employee, on_delete=models.CASCADE)
    address_type    = models.CharField(max_length=20, choices=ADDRESS_TYPE)
    address         = models.CharField(max_length=120)
    village         = models.CharField(max_length=32)
    district        = models.CharField(max_length=32)
    city            = models.CharField(max_length=32)
    province        = models.CharField(max_length=32)

    class Meta:
        """Meta definition for Employee_address."""

        verbose_name = 'Employee_address'
        verbose_name_plural = 'Employee_addresss'

    def __str__(self):
        """Unicode representation of Employee_address."""
        return f"{self.employee}-{self.address_type}-{self.address}-{self.village}-{self.district}-{self.city}-{self.province}"

class Employee_family(models.Model):
    """Model definition for Employee_family."""
    FAMILY_RELATION = [
        ('child', 'Child'),
        ('father_in_law', 'Father_in_law'),
        ('mother', 'Wife'),
        ('mother_in_law', 'Mother_in_law')
        ('spouse', 'Spouse'),
    ]

    SEX = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    # TODO: Define fields here
    employee        = models.ForeignKey(Employee, on_delete=models.CASCADE)
    name            = models.CharField(max_length=100)
    sex             = models.CharField(max_length=6, choices=SEX)
    relationship    = models.CharField(max_length=10, choices=FAMILY_RELATION)
    date_of_birth   = models.DateField()
    class Meta:
        """Meta definition for Employee_family."""

        verbose_name = 'Employee_family'
        verbose_name_plural = 'Employee_familys'

    def __str__(self):
        """Unicode representation of Employee_family."""
        return f"{self.employee}-{self.relation}-{self.name}-{self.date_of_birth}"
    
class Employee_studied(models.Model):
    """Model definition for Employee_studied."""

    # TODO: Define fields here
    employee            = models.ForeignKey(Employee, on_delete=models.CASCADE)
    institution_name    = models.CharField(max_length=100)
    graduation_year     = models.PositiveSmallIntegerField(
                            validators=[MinValueValidator(1900), MaxValueValidator(2100)],
                            null=True,
                            blank=True
                        )
    major               = models.CharField(max_length=100, null=True, blank=True)
    degree              = models.CharField(max_length=8, null=True, blank=True)
    class Meta:
        """Meta definition for Employee_studied."""

        verbose_name = 'Employee_studied'
        verbose_name_plural = 'Employee_studieds'

    def __str__(self):
        """Unicode representation of Employee_studied."""
        return f"{self.employee}-{self.institution_name}-{self.graduation_year}-{self.major}-{self.degree}"

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
        return f"{self.name}{self.level}{self.grade}"


class Employee_history(models.Model):
    """Model definition for Employee_history."""

    # TODO: Define fields here
    employee            = models.ForeignKey(Employee, on_delete=models.CASCADE)
    subdepartement      = models.ForeignKey(Subdepartement, ondelete=models.CASCADE)
    position            = models.ForeignKey(Position, on_delete=models.CASCADE)
    grade               = models.CharField(max_length=3, null=True, blank=True)
    class Meta:
        """Meta definition for Employee_history."""

        verbose_name = 'Employee_history'
        verbose_name_plural = 'Employee_historys'

    def __str__(self):
        """Unicode representation of Employee_history."""
        pass
