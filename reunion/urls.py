from django.urls import path

from reunion.views import IndexView, LoginView, PanelView, CrearReunionView, LogoutView, UnirmeView, ReunionLibreView, \
    DetalleView, ListaSalaView, ListaEstudianteView, CrearEstudianteView, CrearSalaView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('unirme', UnirmeView.as_view(), name='unirme'),
    path('panel', PanelView.as_view(), name='panel'),
    path('panel/crear_reunion', CrearReunionView.as_view(), name='crear_reunion'),
    path('panel/reunion_libre', ReunionLibreView.as_view(), name='reunion_libre'),
    path('panel/detalle_reunion', DetalleView.as_view(), name='detalle_reunion'),
    path('panel/lista_sala', ListaSalaView.as_view(), name='lista_sala'),
    path('panel/crear_sala', CrearSalaView.as_view(), name='crear_sala'),
    path('panel/lista_estudiante', ListaEstudianteView.as_view(), name='lista_estudiante'),
    path('panel/crear_estudiante', CrearEstudianteView.as_view(), name='crear_estudiante'),
]
