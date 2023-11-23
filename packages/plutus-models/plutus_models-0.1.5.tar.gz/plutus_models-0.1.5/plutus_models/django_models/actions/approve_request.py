from django.db import models


class ApproveRequest(models.Model):
    """
    The model is responsible for accepting to join the channel.
    """
    class Quantity(models.TextChoices):
        FIRST = "First"
        ALL = "All"

    quantity = models.CharField(choices=Quantity.choices)

    class Meta:
        db_table = "approve_request"
