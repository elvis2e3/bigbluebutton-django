
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView as LoginViewDjango, LogoutView as LogoutViewDjango
from django.contrib.auth.models import User, Group
from hashlib import sha1

# Create your views here.
from django.views.generic import TemplateView, FormView, ListView, DeleteView, UpdateView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

from bigbluebutton.models import BBBMeeting
from reunion.forms import CrearReunionForm, UnirmeForm, CrearUsuarioForm, CrearSalaForm, CrearDirectorForm, \
    EditarDirectorForm, EntidadForm, EditarProfesorForm, CrearProfesorForm
from reunion.models import Sala, Usuario, Entidad


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


# ============== Reuniones ========================


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


# ============== Directores =======================


class ListaDirectoresView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Usuario
    template_name = "lista_directores.html"
    permission_required = 'reunion.view_director'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Usuario.objects.filter(user__groups__name="Director")
        return context


class CrearDirectorView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "form_director.html"
    form_class = CrearDirectorForm
    success_url = '/panel/lista_directores'
    permission_required = 'reunion.add_director'

    def form_valid(self, form):
        form_data = form.cleaned_data
        usuario = form_data['usuario']
        password = form_data['password']
        user = User.objects.create_user(
            username=usuario,
            email="",
            password=password
        )
        user.groups.add(Group.objects.get(name="Director"))
        usuario = Usuario.objects.create(user=user)
        usuario.__dict__.update(form_data)
        usuario.save()
        messages.success(self.request, 'Se creo un nuevo director.')
        return super().form_valid(form)


class EditarDirectorView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "form_director.html"
    form_class = EditarDirectorForm
    success_url = '/panel/lista_directores'
    permission_required = 'reunion.change_director'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_director = self.kwargs["id_director"]
        initial = get_object_or_404(Usuario, id=id_director)
        form = self.form_class(initial=initial.__dict__)
        context['form'] = form
        context['editar'] = True
        context['director'] = initial
        return context

    def form_valid(self, form):
        id_director = self.kwargs["id_director"]
        usuario = get_object_or_404(Usuario, id=id_director)
        form_data = form.cleaned_data
        usuario.__dict__.update(form_data)
        usuario.save()
        messages.success(self.request, 'Se edito correctamente al usuario director.')
        return super().form_valid(form)


class EliminarDirector(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = User
    template_name = "eliminar_director.html"
    success_url = "/panel/lista_directores"
    permission_required = 'reunion.delete_director'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "El director fue eliminado correctamente.")
        return super(EliminarDirector, self).delete(request, *args, **kwargs)


# ============== Entidades ========================


class ListaEntidadesView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Entidad
    template_name = "lista_entidades.html"
    permission_required = 'reunion.view_entidad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.groups.all()[0].name=="Admin":
            context['object_list'] = Entidad.objects.all()
        elif self.request.user.groups.all()[0].name=="Director":
            context['object_list'] = Entidad.objects.filter(encargado__user=self.request.user)
        elif self.request.user.groups.all()[0].name=="Profesor":
            context['object_list'] = Entidad.objects.filter(miembros__user=self.request.user)
        else:
            context['object_list'] = []
        return context


class CrearEntidadView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "form_entidad.html"
    form_class = EntidadForm
    success_url = '/panel/lista_entidades'
    permission_required = 'reunion.add_entidad'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Se creo una nueva Entidad Educativa.')
        return super().form_valid(form)

class EditarEntidadView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = "form_entidad.html"
    model = Entidad
    form_class = EntidadForm
    success_url = '/panel/lista_entidades'
    permission_required = 'reunion.change_entidad'

    def get_initial(self):
        initial = super().get_initial()
        initial['nombre'] = self.object.nombre
        initial['encargado'] = self.object.encargado
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_entidad = self.kwargs["pk"]
        initial = get_object_or_404(Entidad, id=id_entidad)
        context['editar'] = True
        context['entidad'] = initial
        return context

    def form_valid(self, form):
        messages.success(self.request, 'La Entidad Educativa se edito correctamente.')
        return super().form_valid(form)


class EliminarEntidad(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Entidad
    template_name = "eliminar_entidad.html"
    success_url = "/panel/lista_entidades"
    permission_required = 'reunion.delete_entidad'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "La Entidad Educativa fue eliminada correctamente.")
        return super(EliminarEntidad, self).delete(request, *args, **kwargs)


# ============== Profesores =======================


class ListaProfesoresView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Usuario
    template_name = "lista_profesores.html"
    permission_required = 'reunion.view_profesor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Usuario.objects.filter(user__groups__name="Profesor")
        return context


class CrearProfesorView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "form_profesor.html"
    form_class = CrearProfesorForm
    success_url = '/panel/lista_profesores'
    permission_required = 'reunion.add_profesor'

    def form_valid(self, form):
        form_data = form.cleaned_data
        usuario = form_data['usuario']
        password = form_data['password']
        user = User.objects.create_user(
            username=usuario,
            email="",
            password=password
        )
        user.groups.add(Group.objects.get(name="Profesor"))
        usuario = Usuario.objects.create(user=user)
        usuario.__dict__.update(form_data)
        usuario.save()
        messages.success(self.request, 'Se creo un nuevo profesor.')
        return super().form_valid(form)


class EditarProfesorView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "form_profesor.html"
    form_class = EditarProfesorForm
    success_url = '/panel/lista_profesores'
    permission_required = 'reunion.change_profesor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_profesor = self.kwargs["id_profesor"]
        initial = get_object_or_404(Usuario, id=id_profesor)
        form = self.form_class(initial=initial.__dict__)
        context['form'] = form
        context['editar'] = True
        context['profesor'] = initial
        return context

    def form_valid(self, form):
        id_profesor = self.kwargs["id_profesor"]
        usuario = get_object_or_404(Usuario, id=id_profesor)
        form_data = form.cleaned_data
        usuario.__dict__.update(form_data)
        usuario.save()
        messages.success(self.request, 'Se edito correctamente al usuario profesor.')
        return super().form_valid(form)


class EliminarProfesor(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = User
    template_name = "eliminar_profesor.html"
    success_url = "/panel/lista_profesores"
    permission_required = 'reunion.delete_profesor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "El profesor fue eliminado correctamente.")
        return super(EliminarProfesor, self).delete(request, *args, **kwargs)


# ============


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
