from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('panel-note-detail', kwargs={'pk': self.pk})


# class Comment(models.Model):
#     user = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     note = models.ForeignKey(Note, on_delete=models.CASCADE)
#     content = models.TextField(max_length=300)
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.pk)


# class Course(models.Model):
#     name = models.CharField(max_length=100)
#     leader = models.ForeignKey(User, on_delete=models.CASCADE)
#     students = models.ManyToManyField(User)
#     notes = models.ManyToManyField(Note)
