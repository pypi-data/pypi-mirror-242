from django.db import models


class Token(models.Model):
    """Token model."""
    token = models.UUIDField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "token"

    def __str__(self):
        return str(self.token)
