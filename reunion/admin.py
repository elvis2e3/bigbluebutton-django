from django.contrib import admin

# Register your models here.
from reunion.models import Sala, Usuario, Entidad

admin.site.register(Sala)
admin.site.register(Usuario)
admin.site.register(Entidad)
