from django.db import models


class UserEvent(models.Model):
    user = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True)
    event = models.ForeignKey("Event", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_events"
