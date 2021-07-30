from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as LoginViewDjango
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"


class LoginView(LoginViewDjango):
    template_name = "login.html"


class PanelView(LoginRequiredMixin, TemplateView):
    template_name = "panel_reunion.html"


class CrearReunionView(LoginRequiredMixin, TemplateView):
    template_name = "crear_reunion.html"