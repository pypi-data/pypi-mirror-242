from django.db import models


class ChatAction(models.Model):
    """
    Model to tell the user that something is going on the bot's side.
    The status is set for 5 seconds or less
        (when a message arrives from your bot, Telegram clients clear its typing status)
    """
    class Actions(models.TextChoices):
        TYPING = "Typing"
        UPLOAD_PHOTO = "Upload photo"
        UPLOAD_VIDEO = "Upload video"
        RECORD_VIDEO = "Record video"
        UPLOAD_VOICE = "Upload voice"
        RECORD_VOICE = "Record voice"
        UPLOAD_DOCUMENT = "Upload document"
        UPLOAD_VIDEO_NOTE = "Upload video note "
        RECORD_VIDEO_NOTE = "Record video note"

    chat_action = models.CharField(choices=Actions.choices)

    duration = models.IntegerField(default=5)

    class Meta:
        db_table = "chat_action"
