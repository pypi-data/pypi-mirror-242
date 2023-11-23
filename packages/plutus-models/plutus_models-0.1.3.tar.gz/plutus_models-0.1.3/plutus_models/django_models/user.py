from django.db import models

from .action import Action
from .block import Block
from .bot import Bot
from .event import Event
from .frozen_user_event import FrozenUserEvent
from .spammer import Spammer


class User(models.Model):
    uid = models.BigIntegerField(null=False)
    username = models.CharField(max_length=32, null=True, blank=True)
    first_name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    params = models.TextField(max_length=64, null=True, blank=True)
    status = models.BooleanField(default=True)
    spammer = models.ManyToManyField(Spammer, through="UsersSpammer")
    bot = models.ForeignKey(Bot, on_delete=models.SET_NULL, null=True, blank=True)
    block = models.ForeignKey(Block, on_delete=models.SET_NULL, null=True, blank=True)
    events = models.ManyToManyField(Event, through="UserEvent", related_name="user_events")
    frozen_events = models.ManyToManyField(
        Event, through=FrozenUserEvent, related_name="frozen_events")

    def __str__(self):
        return self.first_name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_bot_uid", fields=["uid", "bot"]
            )
        ]
        db_table = "user"


class UsersSpammer(models.Model):
    status = models.BooleanField(default=None, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    spammer = models.ForeignKey(Spammer, on_delete=models.SET_NULL, null=True, blank=True)
    bot = models.ForeignKey(Bot, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.ForeignKey(Action, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.firstname

    class Meta:
        db_table = "users_spammer"
