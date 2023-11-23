from django.db import models

from .bot import Bot


class GroupBot(models.Model):
    title = models.CharField(max_length=64)
    bots = models.ManyToManyField(Bot, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "group_bot"
