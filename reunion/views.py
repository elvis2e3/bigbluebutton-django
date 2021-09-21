
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as LoginViewDjango, LogoutView as LogoutViewDjango
from django.contrib.auth.models import User, Group
from hashlib import sha1

# Create your views here.
from django.views.generic import TemplateView, FormView, ListView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect

from bigbluebutton.models import BBBMeeting
from reunion.forms import CrearReunionForm, UnirmeForm, CrearUsuarioForm, CrearSalaForm
from reunion.models import Sala


def unirme_a_reunion(self, form):
    form_data = form.cleaned_data
    codigo_reunion = form_data['codigo_reunion']
    nombre_usuario = form_data['nombre_usuario']
    open_meetings = []
    try:
        bbb_meeting = BBBMeeting.get_meetings_list()
    except:
        bbb_meeting = []
    for meet in bbb_meeting:
        open_meetings.append(meet['meetingID'])
    if codigo_reunion in open_meetings:
        join_url = BBBMeeting.join_meeting(codigo_reunion, "estudiante", nombre_usuario)
        return True, join_url
    else:
        return False, ""


class IndexView(TemplateView):
    template_name = "index.html"


class UnirmeView(FormView):
    form_class = UnirmeForm
    template_name = "unirme.html"
    success_url = '/unirme'

    def form_valid(self, form):
        existe_reunion, unirme_url = unirme_a_reunion(self, form)
        if existe_reunion:
            return redirect(unirme_url)
        else:
            messages.warning(self.request,
                             'El codigo de reunion no es correcto o no se encuentra activo en este momento!.')
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
            messages.warning(self.request, 'Tenemos problemas de conexion.')
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
            attendeePW="estudiante",
            moderatorPW=group_name,
            duration=meeting_duration,
            record=True,
            allowStartStopRecording=True,
            welcome=meeting_name,
            running=True
        )
        messages.success(self.request, 'Se creo una nueva reunion.')
        return super().form_valid(form)


class ReunionLibreView(LoginRequiredMixin, FormView):
    template_name = "reunion_libre.html"
    form_class = UnirmeForm
    success_url = '/panel/reunion_libre'

    def form_valid(self, form):
        unirme_a_reunion(self, form)
        existe_reunion, unirme_url = unirme_a_reunion(self, form)
        if existe_reunion:
            return redirect(unirme_url)
        else:
            messages.warning(self.request,
                             'El codigo de reunion no es correcto o no se encuentra activo en este momento!.')
        return super().form_valid(form)


class CrearSalaView(FormView):
    form_class = CrearSalaForm
    template_name = "crear_aula.html"
    success_url = '/panel/lista_aula'

    def form_valid(self, form):
        form.instance.moderador = self.request.user
        form.save()
        return super().form_valid(form)


class DetalleView(TemplateView):
    template_name = "detalle_reunion.html"


class ListaSalaView(ListView):
    model = Sala
    template_name = "lista_aulas.html"


class CrearEstudianteView(FormView):
    form_class = CrearUsuarioForm
    template_name = "crear_estudiante.html"
    success_url = '/panel/lista_estudiante'

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name='estudiante')
        group.user_set.add(user)
        return super().form_valid(form)


class ListaEstudianteView(ListView):
    model = User
    template_name = "lista_estudiantes.html"
