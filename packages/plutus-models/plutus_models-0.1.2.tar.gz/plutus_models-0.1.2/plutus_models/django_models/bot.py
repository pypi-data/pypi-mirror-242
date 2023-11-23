from django.db import models

from .dialogue import Dialogue
from .var import Var
from .validatots.token_validator import token_validator_runner


class Bot(models.Model):
    title = models.CharField(max_length=64)
    uid = models.BigIntegerField(null=False)
    token = models.CharField(
        max_length=128, validators=[token_validator_runner]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    dialog = models.ForeignKey(Dialogue, on_delete=models.SET_NULL, null=True, blank=True)
    vars = models.ManyToManyField(Var, blank=True)
    enable = models.BooleanField(default=True)

    trigger_on_start = models.BooleanField(default=True)
    trigger_on_join_request = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "bot"
