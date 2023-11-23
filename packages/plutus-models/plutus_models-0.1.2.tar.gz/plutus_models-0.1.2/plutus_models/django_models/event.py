from django.db import models

from .mind import Mind


class Event(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64)

    """
    Joined or left the channel
    """

    class ChatMemberType(models.TextChoices):
        JOIN = "Join"
        LEAVE = "Leave"
        REQUEST = "Request"

    chat_member = models.CharField(
        choices=ChatMemberType.choices, null=True, blank=True,
        help_text="Triggered if the user has join/leave the channel in which the bot is the administrator")

    """
    Webhook from partners
    """
    class Webhook(models.TextChoices):
        REG = "Registration"
        FD = "First deposit"
        DEP = "Deposit"

    webhook = models.CharField(choices=Webhook.choices, null=True, blank=True,
                               help_text="Triggered by responses from the affiliate program")

    """
    Do it after a while
    """
    timer = models.DurationField(null=True, blank=True,
                                 help_text="The timer starts from the moment the user creates the event")

    """
    Message from the user
    """
    message = models.TextField(max_length=1024, null=True, blank=True,
                               help_text="The message that the user must send in order for the event to trigger. "
                                         "You can use regular expressions.")

    """
    Callback data from inline button
    """
    callback = models.CharField(max_length=64, null=True, blank=True,
                                help_text="Callback data from the inline button")

    mind = models.ForeignKey(Mind, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "event"
