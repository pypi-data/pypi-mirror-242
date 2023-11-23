from .base import BaseParameters, MediaABC, TextABC, ThumbnailABC


class DocumentMessage(BaseParameters, MediaABC, TextABC, ThumbnailABC):
    """
    Model to send general files
    """

    class Meta:
        db_table = "document_message"
