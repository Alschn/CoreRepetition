from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from PIL import Image
from CoreRepetition.panel.models import Course
from .utils import get_random_code


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    courses = models.ManyToManyField(Course, blank=True, null=True, related_name='courses')

    def __str__(self):
        return f"{self.user.username} Profile - {self.created.strftime('%d/%m/%Y-%H:%M')}"

    def get_friends(self):
        return self.friends.all()

    def get_friends_count(self):
        return self.friends.all().count()

    def get_courses(self):
        return self.courses.all()

    def get_courses_count(self):
        return self.courses.all().count()

    def get_notes(self):
        return self.user.notes.all()

    def get_notes_count(self):
        # related name = notes
        return self.user.notes.all().count()

    def save(self, *args, **kwargs):
        exists = False
        if self.first_name and self.last_name:
            to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
            exists = Profile.objects.filter(slug=to_slug).exists()
            while exists:
                to_slug = slugify(to_slug + " " + str(get_random_code()))
                exists = Profile.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.user)
        self.slug = to_slug

        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
