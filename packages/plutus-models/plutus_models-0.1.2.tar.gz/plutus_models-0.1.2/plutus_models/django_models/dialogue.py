from django.db import models

from .block import Block


class Dialogue(models.Model):
    title = models.CharField(max_length=64)

    start_block = models.ForeignKey(Block, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "dialogue"
