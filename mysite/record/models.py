from django.db import models


# Create your models here.
from django.utils import timezone


class Todolist(models.Model):
    created_time = models.DateTimeField(default=timezone.now)
    updated_time=models.DateTimeField(auto_now=True)
    body = models.TextField()
    feed_back=models.TextField(blank=True,default="unfinished")
    is_done = models.BooleanField(default=False)

    class Meta:
        ordering = ('-updated_time',)
