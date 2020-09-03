from django.urls import path
from . import views


urlpatterns = [
    path('', views.panel_main, name='panel-main'),
    path('courses/', views.panel_courses, name='panel-courses'),
]
