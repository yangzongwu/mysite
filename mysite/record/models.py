from django.db import models


# Create your models here.
from django.utils import timezone


class Todolist(models.Model):
    created_time = models.DateTimeField(default=timezone.now)
    body = models.TextField()
    is_done = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_time',)
