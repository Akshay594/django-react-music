from django.db import models
from django.contrib.auth import get_user_model

user_model = get_user_model()


class Track(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    posted_by = models.ForeignKey(
        user_model, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(user_model, on_delete=models.CASCADE, null=True)
    track = models.ForeignKey(
        Track, on_delete=models.CASCADE, related_name='likes')
