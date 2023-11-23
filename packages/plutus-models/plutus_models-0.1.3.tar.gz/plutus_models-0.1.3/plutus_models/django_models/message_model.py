from django.db import models


class MessageModel(models.Model):
    """Telegram message model."""

    class ContentType(models.TextChoices):
        MESSAGE = "message"
        APPROVE = "approve"
        CALLBACK = "callback"
        HTTP_REQUEST = "http_request"

    chat_id = models.BigIntegerField()
    bot_id = models.BigIntegerField()
    message_id = models.BigIntegerField(null=True)
    json = models.JSONField()
    is_edited = models.BooleanField(default=False)
    content_type = models.CharField(
        default=ContentType.MESSAGE, choices=ContentType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Actual message (bot{self.bot_id} chat{self.chat_id} "
            f"message{self.message_id})"
        )

    class Meta:
        db_table = "message"
        ordering = ['-created_at']
