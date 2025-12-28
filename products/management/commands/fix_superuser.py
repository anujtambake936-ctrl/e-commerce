from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Fix superuser permissions by ensuring is_staff=True'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username to fix (default: AnujS)',
            default='AnujS',
        )

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
            
            self.stdout.write(f"Found user: {user.username}")
            self.stdout.write(f"Current status:")
            self.stdout.write(f"  - is_superuser: {user.is_superuser}")
            self.stdout.write(f"  - is_staff: {user.is_staff}")
            self.stdout.write(f"  - is_active: {user.is_active}")
            
            updated = False
            
            if not user.is_staff:
                self.stdout.write(f"\nSetting is_staff=True for {username}...")
                user.is_staff = True
                updated = True
                
            if not user.is_superuser:
                self.stdout.write(f"\nSetting is_superuser=True for {username}...")
                user.is_superuser = True
                updated = True
                
            if updated:
                user.save()
                self.stdout.write(self.style.SUCCESS(f'\n✓ Fixed! User "{username}" can now access admin and add products.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'\n✓ User "{username}" already has correct permissions.'))
                
            self.stdout.write(f"\nFinal status:")
            self.stdout.write(f"  - is_superuser: {user.is_superuser}")
            self.stdout.write(f"  - is_staff: {user.is_staff}")
            self.stdout.write(f"  - is_active: {user.is_active}")
            self.stdout.write(self.style.WARNING('\n⚠ Please log out and log back in to the admin for changes to take effect.'))
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" not found!'))
            self.stdout.write('Available users:')
            for u in User.objects.all():
                self.stdout.write(f'  - {u.username}')

