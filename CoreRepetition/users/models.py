from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from PIL import Image
from CoreRepetition.panel.models import Course
from django.db.models import Q
from .utils import get_random_code


class ProfileManager(models.Manager):

    def get_all_profiles_to_invite(self, sender):
        """Gets all the profiles that can be invited by us."""
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))

        accepted = []
        for relationship in qs:
            if relationship.status == 'accepted':
                accepted.append(relationship.receiver)
                accepted.append(relationship.sender)

        # All the profiles which are not in accepted list
        available = [profile for profile in profiles if profile not in accepted]
        return available

    def get_all_profiles_except(self, excluded):
        profiles = Profile.objects.all().exclude(user=excluded)
        return profiles


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

    objects = ProfileManager()

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
    ('sent', 'sent'),
    ('accepted', 'accepted')
)


class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='sent')
        return qs


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
