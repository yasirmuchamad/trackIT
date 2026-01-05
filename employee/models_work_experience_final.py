# Final Work Experience Model - Best Practice

class ExternalCompanyPosition(models.Model):
    """Master data for common positions in external companies"""
    
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, blank=True)  # e.g., "IT", "Finance", "Marketing"
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'External Company Position'
        verbose_name_plural = 'External Company Positions'
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name}" + (f" ({self.category})" if self.category else "")


class ExternalCompanyDepartment(models.Model):
    """Master data for common departments in external companies"""
    
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, blank=True)  # e.g., "Technical", "Business", "Support"
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'External Company Department'
        verbose_name_plural = 'External Company Departments'
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name}" + (f" ({self.category})" if self.category else "")


class WorkExperienceExitReason(models.Model):
    """Standardized exit reasons"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Work Experience Exit Reason'
        verbose_name_plural = 'Work Experience Exit Reasons'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class EmployeeWorkExperience(models.Model):
    """Employee Work Experience - Final Version"""
    
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='work_experiences'
    )
    
    company_name = models.CharField(
        max_length=100,
        help_text="Nama perusahaan tempat bekerja sebelumnya"
    )
    
    # Position - Hybrid approach
    position_standard = models.ForeignKey(
        ExternalCompanyPosition,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Standard Position",
        help_text="Pilih dari daftar posisi umum"
    )
    
    position_custom = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Custom Position",
        help_text="Atau tulis posisi spesifik"
    )
    
    # Department - Hybrid approach
    department_standard = models.ForeignKey(
        ExternalCompanyDepartment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Standard Department",
        help_text="Pilih dari daftar departemen umum"
    )
    
    department_custom = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Custom Department",
        help_text="Atau tulis departemen spesifik"
    )
    
    start_date = models.DateField(help_text="Tanggal mulai bekerja")
    end_date = models.DateField(help_text="Tanggal selesai bekerja")
    
    job_description = models.TextField(
        blank=True,
        help_text="Deskripsi pekerjaan dan tanggung jawab"
    )
    
    # Exit reason - Standardized
    exit_reason = models.ForeignKey(
        WorkExperienceExitReason,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Alasan meninggalkan pekerjaan"
    )
    
    exit_reason_custom = models.CharField(
        max_length=200,
        blank=True,
        help_text="Alasan lain jika tidak ada di daftar"
    )
    
    salary_range = models.CharField(
        max_length=50,
        blank=True,
        help_text="Range gaji (opsional)"
    )
    
    supervisor_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Nama atasan langsung"
    )
    
    supervisor_contact = models.CharField(
        max_length=50,
        blank=True,
        help_text="Kontak atasan (email/telepon)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Employee Work Experience'
        verbose_name_plural = 'Employee Work Experiences'
        ordering = ['-end_date', '-start_date']
        
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_date__lt=models.F('end_date')),
                name='work_experience_dates_valid'
            )
        ]
    
    def clean(self):
        super().clean()
        
        # Validate dates
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValidationError({'end_date': 'End date must be after start date'})
        
        # Validate position: must have either standard or custom
        if not self.position_standard and not self.position_custom:
            raise ValidationError('Either select a standard position or enter a custom position')
        
        # Validate max 3 experiences per employee
        if self.employee_id:
            existing_count = EmployeeWorkExperience.objects.filter(
                employee=self.employee
            ).exclude(pk=self.pk).count()
            
            if existing_count >= 3:
                raise ValidationError('Maximum 3 work experiences allowed per employee')
    
    @property
    def display_position(self):
        """Get position for display"""
        if self.position_standard:
            return str(self.position_standard)
        return self.position_custom or "Not specified"
    
    @property
    def display_department(self):
        """Get department for display"""
        if self.department_standard:
            return str(self.department_standard)
        return self.department_custom or "Not specified"
    
    @property
    def display_exit_reason(self):
        """Get exit reason for display"""
        if self.exit_reason:
            return str(self.exit_reason)
        return self.exit_reason_custom or "Not specified"
    
    @property
    def duration_months(self):
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            return round(delta.days / 30.44)
        return 0
    
    @property
    def duration_years(self):
        months = self.duration_months
        return round(months / 12, 1) if months > 0 else 0
    
    def __str__(self):
        return f"{self.employee.name} - {self.display_position} at {self.company_name}"