from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import SMI


# GROUPS
admin_group = Group.objects.create(name='Admin')
accountant_group = Group.objects.create(name='Accountant')
compliance_group = Group.objects.create(name='ComplianceOfficer')
principal_group = Group.objects.create(name='PrincipalOfficer')

# PERMISSIONS
content_type = ContentType.objects.get_for_model(SMI)
view_permissions = Permission.objects.filter(codename='view_smi', content_type=content_type)
change_permissions = Permission.objects.filter(codename='change_smi', content_type=content_type)

admin_group.permissions.set(view_permissions, change_permissions)
accountant_group.permissions.set(view_permissions, change_permissions)
compliance_group.permissions.set(view_permissions, change_permissions)
principal_group.permissions.set(view_permissions)