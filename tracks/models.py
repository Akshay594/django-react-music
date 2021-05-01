from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model


user = get_user_model()


class Track(models.Model):
    title = models.CharField(max_length=50, null=True)
    description = models.TextField(max_length=200, null=True)
    url = models.URLField()
    created_on = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(user, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Like(models.Model):
    track = models.ForeignKey(
        Track, on_delete=models.CASCADE, related_name='likes')
    liked_by = models.ForeignKey(user, on_delete=models.CASCADE)
