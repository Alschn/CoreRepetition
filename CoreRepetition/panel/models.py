from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.urls import reverse


class Course(models.Model):
    name = models.CharField(max_length=300)
#     leader = models.ForeignKey(User, on_delete=models.CASCADE)
#     students = models.ManyToManyField(User)
#     notes = models.ManyToManyField(Note)

    def __str__(self):
        return f"Course: {self.name}"


class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(
        upload_to='posts',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    liked = models.ManyToManyField(User, blank=True, related_name='likes')
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, blank=True)

    def __str__(self):
        return self.title

    def get_likes_count(self):
        return self.liked.all().count()

    def get_absolute_url(self):
        return reverse('panel-note-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    date_posted = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


LIKE_CHOICES = (
    ('Like', 'like'),
    ('Unlike', 'unlike')
)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    date_updated = models.DateTimeField(auto_now=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"



