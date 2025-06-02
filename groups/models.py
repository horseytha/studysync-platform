from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    university = models.CharField(max_length=200, blank=True)
    major = models.CharField(max_length=100, blank=True)
    year_of_study = models.CharField(max_length=50, blank=True)
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class StudyGroup(models.Model):
    SUBJECT_CHOICES = [
        ('math', 'Mathematics'),
        ('science', 'Science'),
        ('english', 'English'),
        ('history', 'History'),
        ('computer_science', 'Computer Science'),
        ('business', 'Business'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(User, related_name='joined_groups', blank=True)
    max_members = models.IntegerField(default=10)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('group_detail', kwargs={'pk': self.pk})

    @property
    def member_count(self):
        return self.members.count()

class StudySession(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='sessions')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    duration_hours = models.IntegerField(default=2)
    location = models.CharField(max_length=200, blank=True)
    is_online = models.BooleanField(default=False)
    meeting_link = models.URLField(blank=True)
    attendees = models.ManyToManyField(User, related_name='attending_sessions', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.group.name}"

    class Meta:
        ordering = ['date_time']
