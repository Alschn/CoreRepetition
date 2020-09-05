from django.urls import path
from . import views


urlpatterns = [
    path('', views.panel_main, name='panel-main'),
    path('courses/', views.panel_courses, name='panel-courses'),
    path('assignments/', views.panel_assignments, name='panel-assignments'),
]
