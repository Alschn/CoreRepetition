from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Note, Course
from CoreRepetition.users.forms import UserRegisterForm, ProfileUpdateForm


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'panel/main.html'
    context_object_name = 'notes'
    notes_count = 3

    def get_queryset(self):
        """Displays n last notes created by the current user"""
        qs = self.model.objects.all().filter(author=self.request.user)\
            .order_by('-date_posted')[:self.notes_count]
        return qs


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ['course', 'title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    fields = ['course', 'title', 'content', 'image']
    success_url = '/panel'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        note = self.get_object()
        if self.request.user == note.author:
            return True
        return False


class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Note
    success_url = '/panel'

    def test_func(self):
        note = self.get_object()
        if self.request.user == note.author:
            return True
        return False


class CourseDetailView(LoginRequiredMixin, ListView):
    """"View: panel_course"""
    model = Note
    template_name = 'panel/course.html'
    context_object_name = 'notes'
    paginate_by = 5

    def get_queryset(self):
        """SELECT note WHERE note.course IN course"""
        qs = self.model.objects.all().filter(
            course__in=self.request.user.profile.get_courses()).order_by('-date_posted')
        return qs

    # additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # stopgap XD
        context['course'] = list(self.get_queryset())[0].course
        return context


@login_required
def panel_courses(request):
    return render(request, 'panel/courses.html')


@login_required
def panel_assignments(request):
    return render(request, 'panel/assignments.html')


@login_required
def panel_profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, "Your account has been updated!")
            return redirect('panel-profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form,
    }

    return render(request, 'panel/profile.html', context)
