from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):

    MASCULINO = "m"
    FEMENINO = "f"
    CHOICES_GENERO = [
        (MASCULINO, "Masculino"),
        (FEMENINO, "Femenino")
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=200)
    apellido_paterno = models.CharField(max_length=100, null=True, blank=True)
    apellido_materno = models.CharField(max_length=100, null=True, blank=True)
    numero_telefonico = models.IntegerField(default=0)
    carnet_identidad = models.CharField(max_length=100, null=True, blank=True)
    genero = models.CharField(max_length=2, choices=CHOICES_GENERO, default=MASCULINO)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    # estudiante
    rude = models.IntegerField(default=0)
    # docentes
    item = models.IntegerField(default=0)

    def __str__(self):
          return "(%s) %s %s %s" % (self.user, self.nombres, self.apellido_paterno, self.apellido_materno)

    class Meta:
        permissions = [
            ('add_director', 'Crear Director'),
            ('change_director', 'Editar Director'),
            ('delete_director', 'Eliminar Director'),
            ('view_director', 'Listar Directores'),
            ('add_profesor', 'Crear Profesor'),
            ('change_profesor', 'Editar Profesor'),
            ('delete_profesor', 'Eliminar Profesor'),
            ('view_profesor', 'Listar Profesores'),
            ('add_estudiante', 'Crear Estudiante'),
            ('change_estudiante', 'Editar Estudiante'),
            ('delete_estudiante', 'Eliminar Estudiante'),
            ('view_estudiante', 'Listar Estudiantes'),
        ]


class Entidad(models.Model):
    nombre = models.CharField(max_length=100)
    encargado = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='encargado',
        db_column='encargado',
    )
    miembros = models.ManyToManyField(Usuario)

    def __str__(self):
        return self.nombre


class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    miembros = models.ManyToManyField(Usuario)
    moderador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='moderador',
        db_column='moderador',
    )
    entidad = models.ForeignKey(
        Entidad,
        on_delete=models.CASCADE,
        related_name='entidad',
        db_column='entidad',
    )

    def __str__(self):
        return self.nombre