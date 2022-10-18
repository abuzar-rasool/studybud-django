from email.policy import default
from queue import Empty
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    REQUIRED_FIELDS= []

class Topic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(User, related_name='participants')


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated_at','-created_at']

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message[0:50]

    class Meta:
        ordering = ['-updated_at', '-created_at']


