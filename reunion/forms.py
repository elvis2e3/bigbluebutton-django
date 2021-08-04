from django.forms import ModelForm

from bigbluebutton.models import BBBMeeting


class CrearReunionForm(ModelForm):
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
