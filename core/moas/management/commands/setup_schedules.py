from django.core.management.base import BaseCommand
from django_q.models import Schedule


class Command(BaseCommand):
    help = 'Registers scheduled tasks for django-q2 (e.g. daily MOA expiry check).'

    def handle(self, *args, **options):
        # Register daily MOA expiry check (runs once per day)
        schedule, created = Schedule.objects.get_or_create(
            name='daily-moa-expiry-check',
            defaults={
                'func': 'moas.tasks.check_moa_expiry',
                'schedule_type': Schedule.DAILY,
                'repeats': -1,  # run indefinitely
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('[OK] Scheduled daily MOA expiry check.'))
        else:
            self.stdout.write(self.style.WARNING('Schedule "daily-moa-expiry-check" already exists. Skipping.'))

        self.stdout.write(self.style.SUCCESS('All schedules registered.'))
