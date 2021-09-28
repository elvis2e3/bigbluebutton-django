from django.urls import path

from reunion.views import IndexView, LoginView, PanelView, CrearReunionView, LogoutView, UnirmeView, ReunionLibreView, \
    DetalleView, ListaEstudiantesView, CrearEstudianteView, CrearSalaView, ListaDirectoresView, \
    CrearDirectorView, EditarDirectorView, EliminarDirector, ListaEntidadesView, CrearEntidadView, EliminarEntidad, \
    EditarEntidadView, ListaProfesoresView, CrearProfesorView, EditarProfesorView, EliminarProfesor, \
    EditarEstudianteView, EliminarEstudiante, EditarSalaView, EliminarSala, ListaSalasView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    # ============ Reuniones ======================
    path('unirme', UnirmeView.as_view(), name='unirme'),
    path('panel', PanelView.as_view(), name='panel'),
    path('panel/crear_reunion', CrearReunionView.as_view(), name='crear_reunion'),
    path('panel/reunion_libre', ReunionLibreView.as_view(), name='reunion_libre'),
    path('panel/detalle_reunion', DetalleView.as_view(), name='detalle_reunion'),
    # =========== Directores ======================
    path('panel/lista_directores', ListaDirectoresView.as_view(), name='lista_directores'),
    path('panel/crear_director', CrearDirectorView.as_view(), name='crear_director'),
    path('panel/editar_director/<int:id_director>', EditarDirectorView.as_view(), name='editar_director'),
    path('panel/eliminar_director/<pk>/', EliminarDirector.as_view(), name='eliminar_director'),
    # =========== Entidades ========================
    path('panel/lista_entidades', ListaEntidadesView.as_view(), name='lista_entidades'),
    path('panel/crear_entidad', CrearEntidadView.as_view(), name='crear_entidad'),
    path('panel/editar_entidad/<int:pk>', EditarEntidadView.as_view(), name='editar_entidad'),
    path('panel/eliminar_entidad/<pk>/', EliminarEntidad.as_view(), name='eliminar_entidad'),
    # ============ Profesores ======================
    path('panel/lista_profesores', ListaProfesoresView.as_view(), name='lista_profesores'),
    path('panel/crear_profesor', CrearProfesorView.as_view(), name='crear_profesor'),
    path('panel/editar_profesor/<int:id_profesor>', EditarProfesorView.as_view(), name='editar_profesor'),
    path('panel/eliminar_profesor/<pk>/', EliminarProfesor.as_view(), name='eliminar_profesor'),
    # ============ Estudiantes =======================
    path('panel/lista_estudiantes', ListaEstudiantesView.as_view(), name='lista_estudiantes'),
    path('panel/crear_estudiante', CrearEstudianteView.as_view(), name='crear_estudiante'),
    path('panel/editar_estudiante/<int:id_estudiante>', EditarEstudianteView.as_view(), name='editar_estudiante'),
    path('panel/eliminar_estudiante/<pk>/', EliminarEstudiante.as_view(), name='eliminar_estudiante'),
    # ============ Salas ============================
    path('panel/lista_salas', ListaSalasView.as_view(), name='lista_salas'),
    path('panel/crear_sala', CrearSalaView.as_view(), name='crear_sala'),
    path('panel/editar_sala/<int:pk>', EditarSalaView.as_view(), name='editar_sala'),
    path('panel/eliminar_sala/<pk>/', EliminarSala.as_view(), name='eliminar_sala'),
]
