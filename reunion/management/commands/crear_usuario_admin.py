from django.contrib.auth.models import User, Group

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'help text'

    def handle(self, *args, **options):
        group_admin = Group.objects.get(
            name="Admin"
        )

        user_admin = User.objects.create_superuser(
            username="Admin",
            email="admin@admin.com",
            first_name="Administrador",
            password="admin"
        )
        print("Se creo el usuario Admin con la clave de inicio:")
        print("admin")
        print("Nota: Una vez iniciado sesion cambie inmediatamente de clave por la segurida de su informacion.")
        user_admin.groups.add(group_admin)