from django.forms import ModelForm

from bigbluebutton.models import BBBMeeting


class CrearReunionForm(ModelForm):
    class Meta:
        model = BBBMeeting
        fields = [
            "name",
            "duration",
        ]

    # name = models.CharField(max_length=100)
    # meetingID = models.CharField(max_length=100, unique=True)
    # attendeePW = models.CharField(max_length=100)
    # moderatorPW = models.CharField(max_length=100)
    # duration = models.IntegerField(blank=False,  default=None)
    # record= models.BooleanField(blank=False, default=None)
    # allowStartStopRecording = models.BooleanField(blank=False, default=None)
    # welcome = models.CharField(max_length=500, blank=False, default=None)
    # running=models.BooleanField(blank=False, default=False)
