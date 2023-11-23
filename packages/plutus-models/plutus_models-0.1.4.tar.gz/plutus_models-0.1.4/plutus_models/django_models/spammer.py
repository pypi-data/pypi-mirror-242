from django.db import models


class Spammer(models.Model):
    title = models.CharField(max_length=64)
    group_bots = models.ManyToManyField("GroupBot", blank=True)
    bots = models.ManyToManyField("Bot", blank=True)
    blocks = models.ManyToManyField("Block", blank=True)
    action = models.ForeignKey("plutus.Action", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date_from = models.DateTimeField(editable=True, blank=True, null=True)
    date_to = models.DateTimeField(editable=True, blank=True, null=True)
    is_running = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "spammer"
