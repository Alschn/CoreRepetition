from django.shortcuts import render
from django.http import HttpResponse


def panel_main(request):
    return render(request, 'panel/main.html')


def panel_courses(request):
    return render(request, 'panel/courses.html')
    