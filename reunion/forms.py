from django import forms
from django.contrib.auth.models import User

from bigbluebutton.models import BBBMeeting
from reunion.models import Sala, Usuario, Entidad


# ============= Reuniones ========================


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


# ============= Directores ========================


class EditarDirectorForm(forms.Form):
    nombres = forms.CharField(label="Nombre *")
    apellido_paterno = forms.CharField(label="Apellido paterno", required=False)
    apellido_materno = forms.CharField(label="Apellido materno", required=False)
    numero_telefonico = forms.IntegerField(label="Número telefónico", required=False)
    carnet_identidad = forms.CharField(label="Carnet de identidad", required=False)
    genero = forms.ChoiceField(label="Genero", widget=forms.Select(), required=False)
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento", widget=forms.DateInput, required=False)
    item = forms.IntegerField(label="Item", required=False)

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['genero'].choices = Usuario.CHOICES_GENERO
        self.fields['numero_telefonico'].initial = 0
        self.fields['item'].initial = 0


class CrearDirectorForm(EditarDirectorForm):
    usuario = forms.CharField(label="Nombre de usuario *")
    password = forms.CharField(label="Contraseña de usuario *", widget=forms.PasswordInput)

    def clean_usuario(self):
        usuario = self.cleaned_data['usuario']
        if len(User.objects.filter(username=usuario)) > 0:
            raise forms.ValidationError("El nombre del usuario ya esta registrado, intente con otro nombre por favor!")
        return usuario


# ============= Entidades ========================


class EntidadForm(forms.ModelForm):

    class Meta:
        model = Entidad
        miembros = forms.ChoiceField(required=False)
        fields = ('nombre', "encargado", "miembros")

    def __init__(self, *args, **kwargs):
        super(EntidadForm, self).__init__(*args, **kwargs)
        self.fields['encargado'].queryset = Usuario.objects.filter(user__groups__name="Director")
        self.fields['miembros'].queryset = Usuario.objects.filter(user__groups__name__in=("Estudiante", "Profesor"))
        self.fields['miembros'].required = False


# ================ Profesores ========================


class EditarProfesorForm(forms.Form):
    nombres = forms.CharField(label="Nombre *")
    apellido_paterno = forms.CharField(label="Apellido paterno", required=False)
    apellido_materno = forms.CharField(label="Apellido materno", required=False)
    numero_telefonico = forms.IntegerField(label="Número telefónico", required=False)
    carnet_identidad = forms.CharField(label="Carnet de identidad", required=False)
    genero = forms.ChoiceField(label="Genero", widget=forms.Select(), required=False)
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento", widget=forms.DateInput, required=False)
    item = forms.IntegerField(label="Item", required=False)

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['genero'].choices = Usuario.CHOICES_GENERO
        self.fields['numero_telefonico'].initial = 0
        self.fields['item'].initial = 0


class CrearProfesorForm(EditarProfesorForm):
    usuario = forms.CharField(label="Nombre de usuario *")
    password = forms.CharField(label="Contraseña de usuario *", widget=forms.PasswordInput)

    def clean_usuario(self):
        usuario = self.cleaned_data['usuario']
        if len(User.objects.filter(username=usuario)) > 0:
            raise forms.ValidationError("El nombre del usuario ya esta registrado, intente con otro nombre por favor!")
        return usuario


# ================


class CrearUsuarioForm(forms.ModelForm):
    username = forms.RegexField(regex=r'^[\w.@+-]+$', max_length=30, label='Nombre de Usuario')
    email = forms.EmailField(label="Correo electrónico")
    first_name = forms.CharField(label='Nombres')
    last_name = forms.CharField(label='Apellidos')
    password1 = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class CrearSalaForm(forms.ModelForm):
    nombre = forms.CharField(label="Nombre de aula")

    class Meta:
        model = Sala
        fields = ('nombre', "miembros")

    def __init__(self, *args, **kwargs):
        super(CrearSalaForm, self).__init__(*args, **kwargs)
        self.fields["miembros"].queryset = User.objects.filter(groups__name='estudiante')


# class CrearSalaForm(forms.ModelForm):
#     nombre = forms.CharField(label="Nombre de aula")
#
#     class Meta:
#         model = Sala
#         fields = ('nombre', "miembros")
#
#     def __init__(self, *args, **kwargs):
#         super(CrearSalaForm, self).__init__(*args, **kwargs)
#         self.fields["miembros"].queryset = User.objects.filter(groups__name='estudiante')
