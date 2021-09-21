from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    apellido_paterno = models.CharField(max_length=100, null=True, blank=True)
    apellido_materno = models.CharField(max_length=100, null=True, blank=True)
    numero_telefonico = models.IntegerField(default=0)

    def __str__(self):
          return "%s" % self.user


class Entidad(models.Model):
    nombre = models.CharField(max_length=100)
    encargado = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='encargado',
        db_column='encargado',
    )
    miembros = models.ManyToManyField(User)

    def __str__(self):
        return self.nombre


class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    miembros = models.ManyToManyField(User)
    moderador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='moderador',
        db_column='moderador',
    )

    def __str__(self):
        return self.nombre