# market/management/commands/create_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from market.models import MarketData

class Command(BaseCommand):
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **kwargs):
        # Create Admin group
        admin_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            content_type = ContentType.objects.get_for_model(MarketData)
            permissions = Permission.objects.filter(content_type=content_type)
            admin_group.permissions.set(permissions)
            self.stdout.write(self.style.SUCCESS('Admin group created and permissions assigned'))

        # Create Regular User group
        regular_group, created = Group.objects.get_or_create(name='Regular User')
        if created:
            self.stdout.write(self.style.SUCCESS('Regular User group created'))

# Don't forget to run the command:
# python manage.py create_groups
