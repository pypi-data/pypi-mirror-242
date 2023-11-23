from django.db import models


class Chats(models.Model):
    """Dialogue model."""
    bot_id = models.BigIntegerField()
    chat_id = models.BigIntegerField()
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    updated_at = models.DateTimeField()

    def __str__(self):
        return f"Dialogue (bot {self.bot_id} chat{self.chat_id})"

    class Meta:
        db_table = "chats"
        ordering = ['-updated_at']
