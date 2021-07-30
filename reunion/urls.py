from django.urls import path

from reunion.views import IndexView, LoginView, PanelView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login', LoginView.as_view(), name='login'),
    path('panel', PanelView.as_view(), name='panel'),
]
