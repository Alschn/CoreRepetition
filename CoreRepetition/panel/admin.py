from django.contrib import admin
from .models import Note, Comment, Like, Course

admin.site.register(Note)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Course)