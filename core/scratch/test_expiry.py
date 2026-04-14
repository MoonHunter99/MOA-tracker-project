import os
import sys

# Add the project root to sys.path
# Script is in MOA-tracker-project/core/scratch/test_expiry.py
# CWD is MOA-tracker-project/core/
sys.path.append(os.getcwd())

import django
from datetime import date, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from companies.models import Company
from moas.models import MOA
from moas.tasks import check_moa_expiry
from notifications.models import Notification

def run_test():
    print("Starting MOA Expiry Test...")
    
    # 1. Ensure we have an admin user
    admin, created = User.objects.get_or_create(username='testadmin', defaults={'is_staff': True, 'email': 'admin@example.com'})
    if created:
        print(f"Created test admin: {admin.username}")
    
    # 2. Create a company and an expiring MOA
    company, _ = Company.objects.get_or_create(name="Test Expiring Corp", defaults={'website': 'https://example.com'})
    
    # Set expiration to 15 days from now
    expiry_date = date.today() + timedelta(days=15)
    
    moa, moa_created = MOA.objects.get_or_create(
        company=company,
        defaults={
            'date_signed': date.today() - timedelta(days=350),
            'expiration_date': expiry_date,
            'is_active': True,
            'document_file': 'test.pdf' # Placeholder for model validation
        }
    )
    
    if not moa_created:
        moa.expiration_date = expiry_date
        moa.is_active = True
        moa.save()
        print(f"Updated MOA for {company.name} to expire on {expiry_date}")
    else:
        print(f"Created expiring MOA for {company.name}")

    # 3. Clear old notifications for this user/company to avoid "already notified" logic
    Notification.objects.filter(user=admin, title__contains=company.name).delete()
    print("Cleared old notifications.")

    # 4. Run the task
    result = check_moa_expiry()
    print(f"Task Result: {result}")

    # 5. Verify notification
    notif = Notification.objects.filter(user=admin, title__contains=company.name).first()
    if notif:
        print(f"SUCCESS: Notification found: {notif.title}")
        print(f"Message: {notif.message}")
    else:
        print("FAILED: No notification created.")

if __name__ == "__main__":
    run_test()
