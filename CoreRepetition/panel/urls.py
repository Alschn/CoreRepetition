from django.urls import path
from .views import NoteListView, NoteDetailView, NoteCreateView, NoteUpdateView, NoteDeleteView
from . import views


urlpatterns = [
    path('', NoteListView.as_view(), name='panel-main'),
    path('note/<int:pk>/', NoteDetailView.as_view(), name='panel-note-detail'),
    path('note/new/', NoteCreateView.as_view(), name='panel-note-create'),
    path('note/<int:pk>/update/', NoteUpdateView.as_view(), name='panel-note-update'),
    path('note/<int:pk>/delete/', NoteDeleteView.as_view(), name='panel-note-delete'),
    path('courses/', views.panel_courses, name='panel-courses'),
    path('assignments/', views.panel_assignments, name='panel-assignments'),
    path('profile/', views.panel_profile, name='panel-profile'),
]
