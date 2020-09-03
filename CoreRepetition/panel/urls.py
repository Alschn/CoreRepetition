from django.urls import path
from . import views


urlpatterns = [
    path('', views.panel_home, name='panel-home'),
]
