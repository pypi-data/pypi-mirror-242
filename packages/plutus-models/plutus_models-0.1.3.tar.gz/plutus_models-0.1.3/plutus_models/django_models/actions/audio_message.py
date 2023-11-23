from django.db import models

from .base import BaseParameters, MediaABC, TextABC, ThumbnailABC


class AudioMessage(BaseParameters, MediaABC, TextABC, ThumbnailABC):
    """
    Model to send audio files
    """
    performer = models.CharField(max_length=32)
    audio_title = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        db_table = "audio_message"
