from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'home/home.html')


def contact(request):
    return render(request, 'home/contact.html')


def courses(request):
    return render(request, 'home/courses.html')


def teachers(request):
    return render(request, 'home/teachers.html')
