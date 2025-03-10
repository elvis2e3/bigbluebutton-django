# Generated by Django 2.1.5 on 2021-09-28 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reunion', '0007_sala_entidad'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usuario',
            options={'permissions': [('add_director', 'Crear Director'), ('change_director', 'Editar Director'), ('delete_director', 'Eliminar Director'), ('view_director', 'Listar Directores'), ('add_profesor', 'Crear Profesor'), ('change_profesor', 'Editar Profesor'), ('delete_profesor', 'Eliminar Profesor'), ('view_profesor', 'Listar Profesores'), ('add_estudiante', 'Crear Estudiante'), ('change_estudiante', 'Editar Estudiante'), ('delete_estudiante', 'Eliminar Estudiante'), ('view_estudiante', 'Listar Estudiantes')]},
        ),
    ]
