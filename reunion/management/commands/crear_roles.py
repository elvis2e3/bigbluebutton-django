from django.contrib.auth.models import Group, Permission

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'help text'

    def handle(self, *args, **options):
        lista_id_permisos_para_estudiante = [
            "view_usuario",
            "view_bbbmeeting",
            "view_sala",
        ]
        lista_id_permisos_para_profesor = [
            "add_bbbmeeting",
            "change_bbbmeeting",
            "delete_bbbmeeting",
            "add_sala",
            "change_sala",
            "delete_sala",
            "add_usuario",
            "change_usuario",
            "delete_usuario",
        ] + lista_id_permisos_para_estudiante
        lista_id_permisos_para_director = ["view_entidad", "change_entidad"] + lista_id_permisos_para_profesor
        lista_id_permisos_para_admin = ["add_entidad", "delete_entidad"] + lista_id_permisos_para_director
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
        estudiante.permissions.set(Permission.objects.filter(codename__in=lista_id_permisos_para_estudiante))
        profesor.permissions.set(Permission.objects.filter(codename__in=lista_id_permisos_para_profesor))
        director.permissions.set(Permission.objects.filter(codename__in=lista_id_permisos_para_director))
        admin.permissions.set(Permission.objects.filter(codename__in=lista_id_permisos_para_admin))
        print("Se agrego los respectivos permisos a los grupos...")
