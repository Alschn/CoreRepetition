from django.urls import path
from .views import (
    NoteListView,
    NoteDetailView,
    NoteCreateView,
    NoteUpdateView,
    NoteDeleteView,
    ProfileListView)
from . import views


urlpatterns = [
    path('', NoteListView.as_view(), name='panel-main'),
    path('note/<int:pk>/', NoteDetailView.as_view(), name='panel-note-detail'),
    path('note/new/', NoteCreateView.as_view(), name='panel-note-create'),
    path('note/<int:pk>/update/', NoteUpdateView.as_view(), name='panel-note-update'),
    path('note/<int:pk>/delete/', NoteDeleteView.as_view(), name='panel-note-delete'),
    path('courses/', views.panel_courses, name='panel-courses'),
    path('courses/<int:pk>/', views.panel_course, name='panel-course'),
    path('assignments/', views.panel_assignments, name='panel-assignments'),
    path('profile/', views.panel_profile, name='panel-profile'),
    path('invites/', views.panel_received_invites, name='panel-received-invites'),
    path('invites/accept', views.accept_invitation, name='panel-accept-invite'),
    path('invites/reject', views.reject_invitation, name='panel-reject-invite'),
    path('profiles/', ProfileListView.as_view(), name='panel-profiles'),
    path('profiles-to-invite/', views.panel_profiles_to_invite, name='panel_profiles_to_invite'),
    path('send-invite/', views.send_invitation, name='panel-send-invite'),
    path('remove-friend/', views.remove_from_friends, name='panel-remove-friend'),
    path('liked/', views.like_unlike_note, name='panel-like-note-view')
]
