from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home-page'),
    path('contact', views.contact, name='contact'),
    path('teachers', views.teachers, name='teachers'),
    path('courses', views.courses, name='courses'),
]
