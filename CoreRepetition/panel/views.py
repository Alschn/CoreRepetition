from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Note
from CoreRepetition.users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


# @login_required
# def panel_main(request):
#     context = {
#         'notes': Note.objects.all(),
#     }
#     return render(request, 'panel/main.html', context)


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'panel/main.html'
    context_object_name = 'notes'
    ordering = ['-date_posted']


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    fields = ['title', 'content']
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


@login_required
def panel_courses(request):
    return render(request, 'panel/courses.html')


@login_required
def panel_assignments(request):
    return render(request, 'panel/assignments.html')


@login_required
def panel_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated!")
            return redirect('panel-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'panel/profile.html', context)
