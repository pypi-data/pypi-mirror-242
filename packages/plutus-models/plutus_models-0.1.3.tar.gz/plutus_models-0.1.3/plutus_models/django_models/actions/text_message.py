from django.db import models

from .base import BaseParameters, TextABC


class TextMessage(BaseParameters, TextABC):
    """
    Model to send text messages
    """
    disable_web_page_preview = models.BooleanField(default=False)

    class Meta:
        db_table = "text_message"
