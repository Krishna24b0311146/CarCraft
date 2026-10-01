from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Reset krishna admin password"

    def handle(self, *args, **kwargs):
        user = User.objects.get(username="krishna")
        user.set_password("NewPassword@123")
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.stdout.write(
            self.style.SUCCESS("Admin password reset successfully!")
        )