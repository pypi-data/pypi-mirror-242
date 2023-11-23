from django.db import models


class FrozenUserEvent(models.Model):
    """Model with 'frozen' events when user blocks bot."""
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    event = models.ForeignKey(
        "Event", null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "user_frozen_events"
