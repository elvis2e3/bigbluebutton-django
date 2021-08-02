from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as LoginViewDjango
from hashlib import sha1

# Create your views here.
from django.views.generic import TemplateView, FormView

from bigbluebutton.models import BBBMeeting
from reunion.forms import CrearReunionForm


class IndexView(TemplateView):
    template_name = "index.html"


class LoginView(LoginViewDjango):
    template_name = "login.html"


class PanelView(LoginRequiredMixin, TemplateView):
    template_name = "panel_reunion.html"


class CrearReunionView(LoginRequiredMixin, FormView):
    template_name = "crear_reunion.html"
    form_class = CrearReunionForm
    success_url = '/panel'

    def form_valid(self, form):
        user = self.request.user
        group_name = user.groups.values_list('name', flat=True)[0]
        form_data = form.cleaned_data
        meeting_name = form_data['name']
        meeting_duration = form_data['duration']
        code = sha1((str(user.id) + " -" + meeting_name).encode('utf-8')).hexdigest()
        BBBMeeting.objects.create(
            name=meeting_name,
            meetingID=code,
            attendeePW=group_name,
            moderatorPW="estudiante",
            duration=meeting_duration,
            record=True,
            allowStartStopRecording=True,
            welcome=meeting_name,
            running=True
        )
        return super().form_valid(form)
