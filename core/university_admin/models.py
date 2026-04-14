from django.db import models

# Create your models here.


class AdminPermissions(models.Model):
    """
    Proxy model that defines custom permission codenames for the admin portal.
    No database table is created (managed = False).
    These permissions are assigned to Django Groups via the setup_rbac_groups command.
    """
    class Meta:
        managed = False
        default_permissions = ()
        permissions = [
            ('can_export_data', 'Can export CSV data'),
            ('can_generate_endorsement', 'Can generate endorsement letters'),
            ('can_manage_roles', 'Can manage user roles/groups'),
        ]
