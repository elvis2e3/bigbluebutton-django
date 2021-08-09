from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as LoginViewDjango, LogoutView as LogoutViewDjango
from hashlib import sha1

# Create your views here.
from django.views.generic import TemplateView, FormView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect

from bigbluebutton.models import BBBMeeting
from reunion.forms import CrearReunionForm, UnirmeForm


class IndexView(TemplateView):
    template_name = "index.html"


class UnirmeView(FormView):
    form_class = UnirmeForm
    template_name = "unirme.html"
    success_url = '/unirme'

    def form_valid(self, form):
        form_data = form.cleaned_data
        codigo_reunion = form_data['codigo_reunion']
        nombre_usuario = form_data['nombre_usuario']
        reuniones = BBBMeeting.objects.filter(meetingID=codigo_reunion)
        if reuniones.exists():
            join_url = BBBMeeting.join_meeting(codigo_reunion, "estudiante", nombre_usuario)
            return redirect(join_url)
        else:
            messages.warning(self.request, 'El codigo de reunion no es correcto, por favor introduzca un codigo valido!.')
        return super().form_valid(form)


class LoginView(LoginViewDjango):
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('panel'))
        return super().get(request, *args, **kwargs)


class LogoutView(LoginRequiredMixin, LogoutViewDjango):
    pass

class PanelView(LoginRequiredMixin, TemplateView):
    template_name = "panel_reunion.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PanelView, self).get_context_data(**kwargs)

        open_meetings = []
        try:
            bbb_meeting = BBBMeeting.get_meetings_list()
        except:
            bbb_meeting = []
        db_meeting = BBBMeeting.objects.all().order_by('meetingID')
        filtro = []

        bbb_meeting_dict = {}
        for meet in bbb_meeting:
            bbb_meeting_dict[meet['meetingID']] = meet
            open_meetings.append(meet['meetingID'])

        for meet in db_meeting:
            if meet.meetingID in bbb_meeting_dict:
                filtro.append(meet)

        context['open_meetings'] = open_meetings
        context['live_meetings'] = filtro
        context['meetingsdb'] = db_meeting

        return context



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
        messages.success(self.request, 'Se creo una nueva reunion.')
        return super().form_valid(form)


class ReunionLibreView(LoginRequiredMixin, TemplateView):
    template_name = "reunion_libre.html"