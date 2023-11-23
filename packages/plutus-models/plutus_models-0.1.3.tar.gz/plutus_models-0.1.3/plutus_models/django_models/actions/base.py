from django.db import models


class BaseParameters(models.Model):
    """
    Abstract model of basic parameters
    """
    title = models.CharField(max_length=128)
    changed_at = models.DateTimeField(auto_now=True)

    disable_notification = models.BooleanField(default=False)
    protect_content = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class MediaABC(models.Model):
    """
    Abstract model for adding a file
    """
    file = models.FileField(upload_to="uploads/",
                            help_text="10 MB max size for photos, 50 MB for other files.")

    class Meta:
        abstract = True


class TextABC(models.Model):
    """
    Abstract model for specifying text
    """
    text = models.TextField(max_length=1024, blank=True, null=True)

    class Meta:
        abstract = True


class ThumbnailABC(models.Model):
    """
    Abstract model for adding a thumbnail
    """
    thumbnail = models.FileField(upload_to="uploads/", null=True, blank=True)

    class Meta:
        abstract = True
