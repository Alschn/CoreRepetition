from django.contrib import admin
from .models import Note, Comment, Like

admin.site.register(Note)
admin.site.register(Comment)
admin.site.register(Like)
