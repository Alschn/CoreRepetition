from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Comment(models.Model):
    content = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.ManyToManyField(Comment)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('panel-note-detail', kwargs={'pk': self.pk})


# class Course(models.Model):
#     name = models.CharField(max_length=100)
#     leader = models.ForeignKey(User, on_delete=models.CASCADE)
#     students = models.ManyToManyField(User)
#     notes = models.ManyToManyField(Note)
