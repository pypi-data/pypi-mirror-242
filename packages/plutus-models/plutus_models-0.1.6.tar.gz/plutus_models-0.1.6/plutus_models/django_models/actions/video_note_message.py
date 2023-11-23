from .base import BaseParameters, MediaABC, TextABC, ThumbnailABC


class VideoNoteMessage(BaseParameters, MediaABC, TextABC, ThumbnailABC):
    """
    Model to send video messages
    """

    class Meta:
        db_table = "video_note_message"
