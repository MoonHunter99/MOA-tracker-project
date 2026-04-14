from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Creates the Coordinator and Department Head groups with their assigned permissions. Idempotent — safe to run multiple times.'

    def handle(self, *args, **options):
        # Ensure the content type for our custom permissions exists
        # The permissions are defined in university_admin.AdminPermissions.Meta.permissions
        ct = ContentType.objects.get(app_label='university_admin', model='adminpermissions')

        # Fetch (or create) permissions
        can_export, _ = Permission.objects.get_or_create(
            codename='can_export_data',
            content_type=ct,
            defaults={'name': 'Can export CSV data'}
        )
        can_endorse, _ = Permission.objects.get_or_create(
            codename='can_generate_endorsement',
            content_type=ct,
            defaults={'name': 'Can generate endorsement letters'}
        )
        can_manage_roles, _ = Permission.objects.get_or_create(
            codename='can_manage_roles',
            content_type=ct,
            defaults={'name': 'Can manage user roles/groups'}
        )

        # --- Coordinator Group ---
        # Day-to-day operations: view dashboard, manage MOAs, manage apps,
        # send messages, view evaluations. No export, endorse, or role management.
        coordinator, created = Group.objects.get_or_create(name='Coordinator')
        coordinator.permissions.clear()
        # Coordinators have no special restricted-action permissions.
        # They rely on the base is_admin check (is_staff) for dashboard access.
        self.stdout.write(
            self.style.SUCCESS(f"{'Created' if created else 'Updated'} group: Coordinator (base admin access)")
        )

        # --- Department Head Group ---
        # Full control: everything a Coordinator can do PLUS exports,
        # endorsement letters, and role management.
        dept_head, created = Group.objects.get_or_create(name='Department Head')
        dept_head.permissions.clear()
        dept_head.permissions.add(can_export, can_endorse, can_manage_roles)
        self.stdout.write(
            self.style.SUCCESS(f"{'Created' if created else 'Updated'} group: Department Head (full access)")
        )

        self.stdout.write(self.style.SUCCESS('\nRBAC groups configured successfully!'))
        self.stdout.write('Assign staff users to groups via the "Manage Roles" page in the admin portal.')
