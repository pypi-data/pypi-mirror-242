from django.db import models

from .event import Event


class Block(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64)

    events = models.ManyToManyField(Event, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "block"
