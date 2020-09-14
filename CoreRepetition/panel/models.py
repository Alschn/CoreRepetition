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

    def get_absolute_url(self):
        return reverse('panel-course', kwargs={'pk': self.pk})

from CoreRepetition.users.models import Profile

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(
        upload_to='posts',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    liked = models.ManyToManyField(User, blank=True, related_name='likes')
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_current_course(self):
        return self.course_set.first()

    def get_likes_count(self):
        return self.liked.all().count()

    def get_comments(self):
        return self.comment_set.all().order_by('-date_posted')

    def get_comments_count(self):
        # referencing Comment model
        return self.comment_set.all().count()

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
        return f"{self.user}-{self.note}-{self.value}"
