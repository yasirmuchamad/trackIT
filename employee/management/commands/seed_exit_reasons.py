from django.core.management.base import BaseCommand
from employee.models import WorkExperienceExitReason

class Command(BaseCommand):
    help = 'Seed work experience exit reasons'

    def handle(self, *args, **options):
        exit_reasons = [
            {
                'name': 'Career Advancement',
                'description': 'Mencari kesempatan karir yang lebih baik'
            },
            {
                'name': 'Better Salary',
                'description': 'Mendapat tawaran gaji yang lebih baik'
            },
            {
                'name': 'Work-Life Balance',
                'description': 'Mencari keseimbangan hidup yang lebih baik'
            },
            {
                'name': 'Company Restructuring',
                'description': 'Perusahaan melakukan restrukturisasi'
            },
            {
                'name': 'Contract Ended',
                'description': 'Kontrak kerja berakhir'
            },
            {
                'name': 'Personal Reasons',
                'description': 'Alasan pribadi/keluarga'
            },
            {
                'name': 'Relocation',
                'description': 'Pindah lokasi/kota'
            },
            {
                'name': 'Further Education',
                'description': 'Melanjutkan pendidikan'
            },
            {
                'name': 'Health Issues',
                'description': 'Masalah kesehatan'
            },
            {
                'name': 'Company Culture',
                'description': 'Tidak cocok dengan budaya perusahaan'
            },
            {
                'name': 'Terminated',
                'description': 'Diberhentikan oleh perusahaan'
            },
            {
                'name': 'Business Closure',
                'description': 'Perusahaan tutup/bangkrut'
            }
        ]
        
        created_count = 0
        for reason_data in exit_reasons:
            reason, created = WorkExperienceExitReason.objects.get_or_create(
                name=reason_data['name'],
                defaults={'description': reason_data['description']}
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created: {reason.name}")
            else:
                self.stdout.write(f"Exists: {reason.name}")
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} exit reasons')
        )