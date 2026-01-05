# Improved Work Experience Model with proper relationships

class WorkExperienceExitReason(models.Model):
    """Model for standardized exit reasons"""
    
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
    """Model definition for Employee Work Experience - Improved Version."""
    
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='work_experiences'
    )
    
    company_name = models.CharField(
        max_length=100,
        help_text="Nama perusahaan tempat bekerja sebelumnya"
    )
    
    # ✅ IMPROVED: Use FK to Position model
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Posisi/jabatan di perusahaan tersebut"
    )
    
    # For positions not in our Position model
    position_other = models.CharField(
        max_length=100,
        blank=True,
        help_text="Posisi lain jika tidak ada di daftar"
    )
    
    # ✅ IMPROVED: Use FK to Department model  
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Departemen/divisi tempat bekerja"
    )
    
    # For departments not in our Department model
    department_other = models.CharField(
        max_length=100,
        blank=True,
        help_text="Departemen lain jika tidak ada di daftar"
    )
    
    start_date = models.DateField(
        help_text="Tanggal mulai bekerja"
    )
    
    end_date = models.DateField(
        help_text="Tanggal selesai bekerja"
    )
    
    job_description = models.TextField(
        null=True,
        blank=True,
        help_text="Deskripsi pekerjaan dan tanggung jawab"
    )
    
    # ✅ IMPROVED: Use FK to standardized exit reasons
    exit_reason = models.ForeignKey(
        WorkExperienceExitReason,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Alasan meninggalkan pekerjaan"
    )
    
    # For custom exit reasons
    exit_reason_other = models.CharField(
        max_length=200,
        blank=True,
        help_text="Alasan lain jika tidak ada di daftar"
    )
    
    salary_range = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Range gaji (opsional)"
    )
    
    supervisor_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Nama atasan langsung"
    )
    
    supervisor_contact = models.CharField(
        max_length=50,
        null=True,
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
                name='work_experience_start_before_end_improved'
            )
        ]
    
    def clean(self):
        """Validasi custom untuk model"""
        super().clean()
        
        # Validasi tanggal
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValidationError({
                    'end_date': 'Tanggal selesai harus setelah tanggal mulai'
                })
        
        # Validasi position: harus ada salah satu
        if not self.position and not self.position_other:
            raise ValidationError({
                'position_other': 'Pilih posisi dari daftar atau isi posisi lainnya'
            })
        
        # Validasi maksimal 3 pengalaman kerja per employee
        if self.employee_id:
            existing_count = EmployeeWorkExperience.objects.filter(
                employee=self.employee
            ).exclude(pk=self.pk).count()
            
            if existing_count >= 3:
                raise ValidationError(
                    'Maksimal hanya 3 pengalaman kerja yang dapat disimpan per employee'
                )
    
    @property
    def display_position(self):
        """Get position name for display"""
        if self.position:
            return str(self.position)
        return self.position_other or "Not specified"
    
    @property
    def display_department(self):
        """Get department name for display"""
        if self.department:
            return str(self.department)
        return self.department_other or "Not specified"
    
    @property
    def display_exit_reason(self):
        """Get exit reason for display"""
        if self.exit_reason:
            return str(self.exit_reason)
        return self.exit_reason_other or "Not specified"
    
    @property
    def duration_months(self):
        """Menghitung durasi kerja dalam bulan"""
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            return round(delta.days / 30.44)
        return 0
    
    @property
    def duration_years(self):
        """Menghitung durasi kerja dalam tahun"""
        months = self.duration_months
        return round(months / 12, 1) if months > 0 else 0
    
    def __str__(self):
        return f"{self.employee.name} - {self.display_position} at {self.company_name}"