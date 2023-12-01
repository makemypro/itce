from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    participants = models.ManyToManyField(User, related_name='rooms')


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)