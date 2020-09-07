from django.shortcuts import render
from .models import Note

notes = [
    {
        'author': 'Adam',
        'title': 'Things I learned today',
        'content': 'First note content',
        'date_posted': 'September 4, 2020'
    },
    {
        'author': 'Adam',
        'title': 'Interesting lesson',
        'content': 'Second note content',
        'date_posted': 'September 5, 2020'
    }
]


def panel_main(request):
    context = {
        'notes': Note.objects.all(),
    }
    return render(request, 'panel/main.html', context)


def panel_courses(request):
    return render(request, 'panel/courses.html')


def panel_assignments(request):
    return render(request, 'panel/assignments.html')
