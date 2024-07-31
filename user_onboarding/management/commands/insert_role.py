from django.core.management.base import BaseCommand

from user_onboarding.models import Roles


class Command(BaseCommand):
    help = 'Insert data into the database'

    def handle(self, *args, **kwargs):
        roles = ["Patient","Doctor"]
        
        for role_name in roles:
            role, created = Roles.objects.update_or_create(name=role_name)
            if created:
                self.stdout.write(f'Created role: {role.name}')
            else:
                self.stdout.write(f'Updated role: {role.name}')

        self.stdout.write(self.style.SUCCESS('Roles inserted successfully'))
        