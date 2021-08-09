from django import forms

from bigbluebutton.models import BBBMeeting


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
