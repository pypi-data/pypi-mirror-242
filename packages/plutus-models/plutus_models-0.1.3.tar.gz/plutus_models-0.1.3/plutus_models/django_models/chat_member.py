from django.db import models

from .user import User
from .bot import Bot


class ChatMember(models.Model):
    chat_uid = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    bot = models.ForeignKey(Bot, on_delete=models.SET_NULL, null=True, blank=True)
    checked = models.BooleanField(default=False)
    is_request = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    class Meta:
        db_table = "chat_member"
        constraints = [
            models.UniqueConstraint(
                fields=["chat_uid", "user", "bot"],
                name="chat_member_unique_constraints"
            )
        ]
