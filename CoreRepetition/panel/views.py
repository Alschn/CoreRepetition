from django.shortcuts import render
from django.http import HttpResponse


def panel_home(request):
    return HttpResponse('<h1>Panel page</h1>')
