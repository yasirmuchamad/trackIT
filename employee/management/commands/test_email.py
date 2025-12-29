from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Command(BaseCommand):
    help = 'Test email configuration and send test email'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            required=True,
            help='Email address to send test email to',
        )
        parser.add_argument(
            '--check-config',
            action='store_true',
            help='Only check email configuration without sending',
        )

    def handle(self, *args, **options):
        to_email = options['to']
        
        # Check configuration
        self.stdout.write("📧 Checking email configuration...")
        self.stdout.write(f"Backend: {settings.EMAIL_BACKEND}")
        self.stdout.write(f"Host: {settings.EMAIL_HOST}")
        self.stdout.write(f"Port: {settings.EMAIL_PORT}")
        self.stdout.write(f"TLS: {settings.EMAIL_USE_TLS}")
        self.stdout.write(f"User: {settings.EMAIL_HOST_USER}")
        
        # Mask password for security
        password = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
        if password:
            masked_password = password[:4] + '*' * (len(password) - 4)
            self.stdout.write(f"Password: {masked_password}")
        else:
            self.stdout.write("❌ Password: NOT SET")
            return
        
        if options['check_config']:
            return
        
        # Test SMTP connection
        self.stdout.write("\n🔌 Testing SMTP connection...")
        try:
            if getattr(settings, 'EMAIL_USE_SSL', False):
                # Use SMTP_SSL for port 465
                server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
            else:
                # Use regular SMTP with STARTTLS for port 587
                server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                if getattr(settings, 'EMAIL_USE_TLS', False):
                    server.starttls()
            
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.quit()
            self.stdout.write(self.style.SUCCESS("✅ SMTP connection successful"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ SMTP connection failed: {e}"))
            
            # Provide specific troubleshooting for 163.com
            error_str = str(e).lower()
            self.stdout.write("\n💡 163.com SMTP Troubleshooting:")
            
            if 'connection unexpectedly closed' in error_str:
                self.stdout.write("   - Try port 587 with TLS instead of port 465 with SSL")
                self.stdout.write("   - Check if your network/firewall blocks SMTP")
                self.stdout.write("   - 163.com might require authorization code instead of password")
            elif 'authentication failed' in error_str:
                self.stdout.write("   - Enable SMTP in 163.com webmail settings")
                self.stdout.write("   - Generate authorization code (not regular password)")
                self.stdout.write("   - Login to webmail: https://mail.163.com")
            elif 'timeout' in error_str:
                self.stdout.write("   - Network connectivity issue")
                self.stdout.write("   - Try different network or VPN")
            
            self.stdout.write("\n🔄 Alternative configurations to try:")
            self.stdout.write("   1. Port 587 + TLS: EMAIL_PORT=587, EMAIL_USE_TLS=True, EMAIL_USE_SSL=False")
            self.stdout.write("   2. Port 25 + TLS: EMAIL_PORT=25, EMAIL_USE_TLS=True, EMAIL_USE_SSL=False")
            return
        
        # Test Django send_mail
        self.stdout.write(f"\n📤 Sending test email to {to_email}...")
        try:
            result = send_mail(
                subject='🧪 Test Email from TrackIT System',
                message=f'''
Hello!

This is a test email from TrackIT Employee Management System.

If you receive this email, the email configuration is working correctly.

Test Details:
- Sent from: {settings.EMAIL_HOST_USER}
- Backend: {settings.EMAIL_BACKEND}
- Host: {settings.EMAIL_HOST}
- Time: {self.get_current_time()}

Best regards,
TrackIT System
                '''.strip(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[to_email],
                fail_silently=False,
            )
            
            if result == 1:
                self.stdout.write(self.style.SUCCESS(f"✅ Test email sent successfully to {to_email}"))
                self.stdout.write("📋 Please check:")
                self.stdout.write("   1. Inbox folder")
                self.stdout.write("   2. Spam/Junk folder")
                self.stdout.write("   3. Wait a few minutes for delivery")
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Email sent but result was: {result}"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Failed to send test email: {e}"))
            
            # Provide troubleshooting hints
            error_str = str(e).lower()
            if 'authentication failed' in error_str:
                self.stdout.write("\n💡 Troubleshooting hints:")
                self.stdout.write("   - Make sure you're using Gmail App Password (16-digit)")
                self.stdout.write("   - Enable 2-Factor Authentication first")
                self.stdout.write("   - Generate new App Password at: https://myaccount.google.com/apppasswords")
            elif 'connection refused' in error_str:
                self.stdout.write("\n💡 Troubleshooting hints:")
                self.stdout.write("   - Check internet connection")
                self.stdout.write("   - Try different network")
                self.stdout.write("   - Check firewall settings")
            elif 'timeout' in error_str:
                self.stdout.write("\n💡 Troubleshooting hints:")
                self.stdout.write("   - Network might be slow")
                self.stdout.write("   - Try again in a few minutes")

    def get_current_time(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")