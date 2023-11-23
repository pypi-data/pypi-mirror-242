from django.db import models


class EditedMessage(models.Model):
    """Telegram edited message model."""
    message = models.ForeignKey(
        "MessageModel", on_delete=models.CASCADE
    )
    json = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.message.message_id)

    class Meta:
        db_table = "edited_message"
        ordering = ['-created_at']
