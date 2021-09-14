from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Aula(models.Model):
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