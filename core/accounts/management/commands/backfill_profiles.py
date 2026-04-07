from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import StudentProfile

class Command(BaseCommand):
    help = 'Backfills StudentProfile for any existing User that lacks one'

    def handle(self, *args, **kwargs):
        users_without_profile = User.objects.filter(profile__isnull=True)
        count = users_without_profile.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS("All users already have a profile. Nothing to do!"))
            return

        self.stdout.write(f"Found {count} users without a profile. Backfilling...")
        
        for user in users_without_profile:
            StudentProfile.objects.create(user=user)
            self.stdout.write(f"Created profile for: {user.username}")
            
        self.stdout.write(self.style.SUCCESS(f"Successfully backfilled {count} profiles!"))
