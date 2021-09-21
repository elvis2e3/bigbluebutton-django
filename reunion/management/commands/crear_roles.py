from django.contrib.auth.models import Group, Permission

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'help text'

    def handle(self, *args, **options):
        lista_id_permisos_para_estudiante = [4, 12, 40]
        lista_id_permisos_para_profesor = [
            1, 2, 3, 9, 10, 11, 37, 38, 39
                         ] + lista_id_permisos_para_estudiante
        lista_id_permisos_para_director = [6, 8] + lista_id_permisos_para_profesor
        lista_id_permisos_para_admin = [5, 7] + lista_id_permisos_para_director
        estudiante = Group.objects.create(
            name="Estudiante"
        )
        print("El grupo Estudiante fue creado...")
        profesor = Group.objects.create(
            name="Profesor"
        )
        print("El grupo Profesor fue creado...")
        director = Group.objects.create(
            name="Director"
        )
        print("El grupo Director fue creado...")
        admin = Group.objects.create(
            name="Admin"
        )
        print("El grupo Admin fue creado...")
        estudiante.permissions.set(Permission.objects.filter(id__in=lista_id_permisos_para_estudiante))
        profesor.permissions.set(Permission.objects.filter(id__in=lista_id_permisos_para_profesor))
        director.permissions.set(Permission.objects.filter(id__in=lista_id_permisos_para_director))
        admin.permissions.set(Permission.objects.filter(id__in=lista_id_permisos_para_admin))
        print("Se agrego los respectivos permisos a los grupos...")
