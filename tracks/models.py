from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()


class Track(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    posted_by = models.ForeignKey(user, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
