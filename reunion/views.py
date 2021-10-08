
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView as LoginViewDjango, LogoutView as LogoutViewDjango
from django.contrib.auth.models import User, Group
from hashlib import sha1
from django.http import JsonResponse

# Create your views here.
from django.views.generic import TemplateView, FormView, ListView, DeleteView, UpdateView, DetailView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

from bigbluebutton.models import BBBMeeting
from reunion.forms import CrearReunionForm, UnirmeForm, CrearDirectorForm, \
    EditarDirectorForm, EntidadForm, EditarProfesorForm, CrearProfesorForm, EditarEstudianteForm, CrearEstudianteForm, \
    SalaForm, CrearReunionSalaForm
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
        user = self.request.user
        if user.groups.all()[0].name == "Estudiante":
            salas = Sala.objects.filter(miembros=user.usuario)
            reuniones = BBBMeeting.objects.filter(salas__in=salas).order_by('meetingID')
            db_meeting = {}
            for reunion in reuniones:
                db_meeting[reunion.id] = reunion
            db_meeting = db_meeting.values()
        else:
            db_meeting = BBBMeeting.objects.filter(moderador=user.usuario).order_by('meetingID')
        open_meetings = []

        try:
            bbb_meeting = BBBMeeting.get_meetings_list()
        except:
            messages.warning(self.request, 'Tenemos problemas de conexion.')
            bbb_meeting = []
        filtro = []
        bbb_meeting_dict = {}
        for meet in bbb_meeting:
            bbb_meeting_dict[meet['meetingID']] = meet
            open_meetings.append(meet['meetingID'])
        for meet in db_meeting:
            if meet.meetingID in bbb_meeting_dict:
                filtro.append(meet)
        context['live_meetings'] = filtro

        context['open_meetings'] = open_meetings
        context['meetingsdb'] = db_meeting

        return context


class ListaReunionesActivasView(LoginRequiredMixin, DetailView):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.groups.all()[0].name == "Estudiante":
            salas = Sala.objects.filter(miembros=user.usuario)
            reuniones = BBBMeeting.objects.filter(salas__in=salas).order_by('meetingID')
            db_meeting = {}
            for reunion in reuniones:
                db_meeting[reunion.id] = reunion
            db_meeting = db_meeting.values()
        else:
            db_meeting = BBBMeeting.objects.filter(moderador=user.usuario).order_by('meetingID')
        open_meetings = []

        try:
            bbb_meeting = BBBMeeting.get_meetings_list()
        except:
            messages.warning(self.request, 'Tenemos problemas de conexion.')
            bbb_meeting = []
        filtro = []
        bbb_meeting_dict = {}
        for meet in bbb_meeting:
            bbb_meeting_dict[meet['meetingID']] = meet
            open_meetings.append(meet['meetingID'])
        for meet in db_meeting:
            if meet.meetingID in bbb_meeting_dict:
                filtro.append(meet)
        # context['live_meetings'] = filtro


        return JsonResponse({'miembros': "miembros"})


class CrearReunionView(LoginRequiredMixin, FormView):
    template_name = "crear_reunion.html"
    form_class = CrearReunionForm
    success_url = '/panel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"].fields["duration"].initial = 60
        return context

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
            running=True,
            moderador=user.usuario
        )
        messages.success(self.request, 'Se creo una nueva reunion.')
        return super().form_valid(form)


class CrearReunionSalaView(LoginRequiredMixin, FormView):
    template_name = "crear_reunion.html"
    form_class = CrearReunionSalaForm
    success_url = '/panel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            if self.request.user.groups.all()[0].name == "Director":
                usaurio = Usuario.objects.get(user=self.request.user)
                entidad = (Entidad.objects.filter(encargado=usaurio))[0]
                usaurios = entidad.miembros.filter(user__groups__name="Profesor")
                context["form"].fields["salas"].queryset = Sala.objects.filter(moderador__in=usaurios)
            elif self.request.user.groups.all()[0].name != "Admin":
                usaurio = Usuario.objects.get(user=self.request.user)
                context["form"].fields["salas"].queryset = Sala.objects.filter(moderador=usaurio)
        except:
            pass
        context["form"].fields["duration"].initial = 60
        return context

    def form_valid(self, form):
        user = self.request.user
        group_name = user.groups.values_list('name', flat=True)[0]
        form_data = form.cleaned_data
        meeting_name = form_data['name']
        meeting_duration = form_data['duration']
        code = sha1((str(user.id) + " -" + meeting_name).encode('utf-8')).hexdigest()
        salas = form_data['salas']
        bbb = BBBMeeting.objects.create(
            name=meeting_name,
            meetingID=code,
            attendeePW="estudiante",
            moderatorPW=group_name,
            duration=meeting_duration,
            record=True,
            allowStartStopRecording=True,
            welcome=meeting_name,
            running=True,
            moderador=user.usuario
        )
        for sala in salas:
            bbb.salas.add(sala)
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


class DetalleView(LoginRequiredMixin, DeleteView):
    template_name = "detalle_reunion.html"
    model = BBBMeeting
    success_url = "/panel"


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


# ============ Estudiantes ======================


class ListaEstudiantesView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Usuario
    template_name = "lista_estudiantes.html"
    permission_required = 'reunion.view_estudiante'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Usuario.objects.filter(user__groups__name="Estudiante")
        return context


class CrearEstudianteView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "form_estudiante.html"
    form_class = CrearEstudianteForm
    success_url = '/panel/lista_estudiantes'
    permission_required = 'reunion.add_estudiante'

    def form_valid(self, form):
        form_data = form.cleaned_data
        usuario = form_data['usuario']
        password = form_data['password']
        user = User.objects.create_user(
            username=usuario,
            email="",
            password=password
        )
        user.groups.add(Group.objects.get(name="Estudiante"))
        usuario = Usuario.objects.create(user=user)
        usuario.__dict__.update(form_data)
        usuario.save()
        messages.success(self.request, 'Se creo un nuevo estudiante.')
        return super().form_valid(form)


class EditarEstudianteView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "form_estudiante.html"
    form_class = EditarEstudianteForm
    success_url = '/panel/lista_estudiantes'
    permission_required = 'reunion.change_estudiante'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_estudiante = self.kwargs["id_estudiante"]
        initial = get_object_or_404(Usuario, id=id_estudiante)
        form = self.form_class(initial=initial.__dict__)
        context['form'] = form
        context['editar'] = True
        context['estudiante'] = initial
        return context

    def form_valid(self, form):
        id_estudiante = self.kwargs["id_estudiante"]
        usuario = get_object_or_404(Usuario, id=id_estudiante)
        form_data = form.cleaned_data
        usuario.__dict__.update(form_data)
        usuario.save()
        messages.success(self.request, 'Se edito correctamente al usuario estudiante.')
        return super().form_valid(form)


class EliminarEstudiante(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = User
    template_name = "eliminar_estudiante.html"
    success_url = "/panel/lista_estudiantes"
    permission_required = 'reunion.delete_estudiante'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "El estudiante fue eliminado correctamente.")
        return super(EliminarEstudiante, self).delete(request, *args, **kwargs)


# ============== Salas ==============================


class ListaSalasView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Sala
    template_name = "lista_salas.html"
    permission_required = 'reunion.view_sala'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.groups.all()[0].name == "Admin":
            context['object_list'] = Sala.objects.all()
        elif self.request.user.groups.all()[0].name == "Director":
            entidades = Entidad.objects.filter(encargado__user=self.request.user)
            context['object_list'] = Sala.objects.filter(entidad__in=entidades)
        elif self.request.user.groups.all()[0].name == "Profesor":
            context['object_list'] = Sala.objects.filter(moderador__user=self.request.user)
        else:
            context['object_list'] = Sala.objects.filter(miembros__user=self.request.user)
        return context


class CrearSalaView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "form_sala.html"
    form_class = SalaForm
    success_url = '/panel/lista_salas'
    permission_required = 'reunion.add_sala'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            if self.request.user.groups.all()[0].name == "Director":
                usaurio = Usuario.objects.get(user=self.request.user)
                context["form"].fields["entidad"].queryset = Entidad.objects.filter(encargado=usaurio)
            elif self.request.user.groups.all()[0].name != "Admin":
                usaurio = Usuario.objects.get(user=self.request.user)
                context["form"].fields["entidad"].queryset = Entidad.objects.filter(miembros__in=(usaurio,))
        except:
            pass
        context["form"].fields["miembros"].queryset = Usuario.objects.filter(id=0)
        return context

    def form_valid(self, form):
        usuario = Usuario.objects.get(user=self.request.user)
        form.instance.moderador = usuario
        form.save()
        messages.success(self.request, 'Se creo una nueva Sala Educativa.')
        return super().form_valid(form)


class EditarSalaView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = "form_sala.html"
    model = Sala
    form_class = SalaForm
    success_url = '/panel/lista_salas'
    permission_required = 'reunion.change_sala'

    def get_initial(self):
        initial = super().get_initial()
        initial['nombre'] = self.object.nombre
        initial['moderador'] = self.object.moderador
        initial['entidad'] = self.object.entidad
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_sala = self.kwargs["pk"]
        initial = get_object_or_404(Sala, id=id_sala)
        context['editar'] = True
        context['sala'] = initial
        try:
            if self.request.user.groups.all()[0].name == "Director":
                usaurio = Usuario.objects.get(user=self.request.user)
                context["form"].fields["entidad"].queryset = Entidad.objects.filter(encargado=usaurio)
            elif self.request.user.groups.all()[0].name != "Admin":
                usaurio = Usuario.objects.get(user=self.request.user)
                context["form"].fields["entidad"].queryset = Entidad.objects.filter(miembros__in=(usaurio,))
        except:
            pass
        print(initial.entidad)
        context["form"].fields["miembros"].queryset = initial.entidad.miembros.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'La Sala Educativa se edito correctamente.')
        return super().form_valid(form)


class EliminarSala(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Sala
    template_name = "eliminar_sala.html"
    success_url = "/panel/lista_salas"
    permission_required = 'reunion.delete_sala'

    def delete(self, requTemplateViewest, *args, **kwargs):
        messages.success(self.request, "La Sala fue eliminada correctamente.")
        return super(EliminarSala, self).delete(self.request, *args, **kwargs)


class ListaMiembrosEntidadView(LoginRequiredMixin, DetailView):
    def get(self, request, *args, **kwargs):
        id_entidad = self.kwargs["pk"]
        entidad = get_object_or_404(Entidad, pk=id_entidad)
        usuarios = entidad.miembros.all()
        miembros = {}
        for usuario in usuarios:
            miembros[usuario.id] = "%s %s %s" % (usuario.nombres, usuario.apellido_paterno, usuario.apellido_materno)
        return JsonResponse({'miembros': miembros})

# ==============


