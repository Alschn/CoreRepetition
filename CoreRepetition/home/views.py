from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse('<h1>Home page</h1>')


def contact(request):
    return HttpResponse('<h1>Contact page</h1>')


def courses(request):
    return HttpResponse('<h1>Our courses</h1>')


def teachers(request):
    return HttpResponse('<h1>Meet our crew!</h1>')