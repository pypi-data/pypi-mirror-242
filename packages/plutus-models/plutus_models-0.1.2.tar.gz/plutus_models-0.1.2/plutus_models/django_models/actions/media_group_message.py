from django.db import models

from .base import BaseParameters
from .photo_message import PhotoMessage
from .video_message import VideoMessage
from .document_message import DocumentMessage
from .audio_message import AudioMessage


class MediaGroupMessage(BaseParameters):
    """
    Model to send a group of photos, videos, documents or audios as an album.
    Documents and audio files can be only grouped in an album with messages of the same type.
    """

    photos = models.ManyToManyField(PhotoMessage, blank=True)

    videos = models.ManyToManyField(VideoMessage, blank=True)

    documents = models.ManyToManyField(DocumentMessage, blank=True)

    audios = models.ManyToManyField(AudioMessage, blank=True)

    class Meta:
        db_table = "media_group_message"
