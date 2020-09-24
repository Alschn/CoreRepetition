from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
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
from CoreRepetition.users.models import Profile, Relationship


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
    """Viewing all the existing courses."""
    courses = Course.objects.all()
    context = {
        'all_courses': courses,
    }
    return render(request, 'panel/courses.html', context)


@login_required
def panel_assignments(request):
    """Displays all homeworks/tasks assigned to the current user."""
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


@login_required
def panel_received_invites(request):
    """Displays all the received invitations from other users"""
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)
    # object from qs is mapped to object.sender in a new list
    results = list(map(lambda x: x.sender, qs))
    context = {
        'invites': results,
    }

    return render(request, 'panel/invites.html', context)

@login_required
def panel_profiles_to_invite(request):
    """Displays all accounts which are available to be invited"""
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(sender=user)

    context = {
        'profiles': qs,
    }

    return render(request, 'panel/profiles_to_invite.html', context)

@login_required
def panel_profiles_list_view(request):
    """Displays all accounts except ours"""
    user = request.user
    qs = Profile.objects.get_all_profiles_except(excluded=user)

    context = {
        'profiles': qs,
    }

    return render(request, 'panel/profile_list.html', context)

class ProfileListView(LoginRequiredMixin, ListView):
    """Displays all accounts except ours.
    You can add/remove friends here on this view."""

    model = Profile
    template_name = 'panel/profile_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles_except(excluded=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        # Query sets of relationship objects
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)

        rel_receiver = []
        rel_sender = []
        for relation in rel_r:
            rel_receiver.append(relation.receiver.user)
        for relation in rel_s:
            rel_receiver.append(relation.sender.user)

        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender

        return context

@login_required
def send_invitation(request):
    """Sending an invitation to the other user."""
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        relationship = Relationship.objects.create(sender=sender, receiver=receiver, status='sent')
        # stay on the same page
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request, 'panel-main')


@login_required
def remove_from_friends(request):
    """Removing a profile from user's friends."""
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        # more complex relation look up with Q
        relationship = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        relationship.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request, 'panel-main')


@login_required
def accept_invitation(request):
    """Accepting pending invitation."""
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        relationship = get_object_or_404(Relationship, sender=sender, receiver=receiver)

        if relationship.status == "sent":
            relationship.status = "accepted"
            relationship.save()
            return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request, 'panel-received-invites')

@login_required
def reject_invitation(request):
    """Rejecting pending invitation."""
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        relationship = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        relationship.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request, 'panel-received-invites')
