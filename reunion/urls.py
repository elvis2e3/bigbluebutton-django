from django.urls import path

from reunion.views import IndexView, LoginView, PanelView, CrearReunionView, LogoutView, UnirmeView, ReunionLibreView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('unirme', UnirmeView.as_view(), name='unirme'),
    path('panel', PanelView.as_view(), name='panel'),
    path('panel/crear_reunion', CrearReunionView.as_view(), name='crear_reunion'),
    path('panel/reunion_libre', ReunionLibreView.as_view(), name='reunion_libre'),
]
