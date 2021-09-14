from django import forms
from django.contrib.auth.models import User

from bigbluebutton.models import BBBMeeting
from reunion.models import Aula


class CrearReunionForm(forms.ModelForm):
    class Meta:
        model = BBBMeeting
        fields = [
            "name",
            "duration",
        ]
        labels={
            "name": "Nombre de la reunion",
            "duration": "Duracion de la reunion (min)"
        }


class UnirmeForm(forms.Form):
    nombre_usuario = forms.CharField()
    codigo_reunion = forms.CharField()


class CrearUsuarioForm(forms.ModelForm):
    username = forms.RegexField(regex=r'^[\w.@+-]+$', max_length=30, label='Nombre de Usuario')
    email = forms.EmailField(label="Correo electrónico")
    fist_name = forms.CharField(label='Nombres')
    last_name = forms.CharField(label='Apellidos')
    password1 = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = User
        fields = ('username', 'email', 'fist_name', 'last_name', 'password1', 'password2')


class CrearAulaForm(forms.ModelForm):
    nombre = forms.CharField(label="Nombre de aula")

    class Meta:
        model = Aula
        fields = ('nombre', "miembros")

    def __init__(self, *args, **kwargs):
        super(CrearAulaForm, self).__init__(*args, **kwargs)
        self.fields["miembros"].queryset = User.objects.filter(groups__name='estudiante')
