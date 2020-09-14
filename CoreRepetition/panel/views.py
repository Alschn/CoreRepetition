from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Note, Course, Like
from .forms import CommentModelForm
from CoreRepetition.users.forms import UserRegisterForm, ProfileUpdateForm


class NoteListView(LoginRequiredMixin, ListView):
    """Note display in main panel page.\n
    Displays notes by the current user from all of their courses.\n"""

    model = Note
    template_name = 'panel/main.html'
    context_object_name = 'notes'
    notes_count = 3

    def get_queryset(self):
        """Displays n last notes created by the current user."""
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


@login_required
def panel_course(request, pk):
    """Displays notes related to the current course.\n
    Notes can be edited, commented and liked."""

    # Get filtered query_set - only notes from the current course
    notes_list = Note.objects.all().filter(
        course__in=request.user.profile.get_courses()
    ).order_by('-date_posted')

    # Notes pagination
    paginate_by = 3
    page = request.GET.get('page', 1)
    paginator = Paginator(notes_list, paginate_by)

    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)

    # Comment form inside each note
    c_form = CommentModelForm()
    if 'submit_comment' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = request.user
            instance.note = Note.objects.get(id=request.POST.get('note_id'))
            instance.save()
            c_form = CommentModelForm()
            return redirect('panel-course', pk=pk)

    context = {
        'notes': notes,
        'course': notes_list.first().course,
        'c_form': c_form,
    }
    return render(request, 'panel/course.html', context)


@login_required
def like_unlike_note(request):
    user = request.user
    if request.method == 'POST':
        note_id = request.POST.get('note_id')
        note_obj = Note.objects.get(id=note_id)
        course_pk = note_obj.course.id
        if user in note_obj.liked.all():
            note_obj.liked.remove(user)
        else:
            note_obj.liked.add(user)

        like, created = Like.objects.get_or_create(user=user, note_id=note_id)

        if not created:
            if like.value == "Like":
                like.value = "Unlike"
            else:
                like.value = "Like"
        else:
            like.value = "Like"

            note_obj.save()
            like.save()
    return redirect('panel-course', pk=course_pk)

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
