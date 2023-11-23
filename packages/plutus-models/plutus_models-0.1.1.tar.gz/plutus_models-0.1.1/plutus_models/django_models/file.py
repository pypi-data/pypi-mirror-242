from django.db import models


class FileModel(models.Model):
    """File model."""
    message = models.ForeignKey(
        "MessageModel", on_delete=models.SET_NULL, null=True)
    path = models.CharField(max_length=250)
    content_type = models.CharField(max_length=50)

    def __str__(self):
        return self.path

    class Meta:
        db_table = "file"
