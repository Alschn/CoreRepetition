from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Note


@login_required
def panel_main(request):
    context = {
        'notes': Note.objects.all(),
    }
    return render(request, 'panel/main.html', context)


@login_required
def panel_courses(request):
    return render(request, 'panel/courses.html')


@login_required
def panel_assignments(request):
    return render(request, 'panel/assignments.html')


@login_required
def panel_profile(request):
    return render(request, 'panel/profile.html')
