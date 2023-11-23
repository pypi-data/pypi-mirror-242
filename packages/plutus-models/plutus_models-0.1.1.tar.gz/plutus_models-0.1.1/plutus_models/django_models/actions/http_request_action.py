from django.db import models


class HttpRequestAction(models.Model):
    """Http request action."""
    url = models.CharField(
        max_length=250, help_text="url_string")

    class Meta:
        db_table = "http_request"
