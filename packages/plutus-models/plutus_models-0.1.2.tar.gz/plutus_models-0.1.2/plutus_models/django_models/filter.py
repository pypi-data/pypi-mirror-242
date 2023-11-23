from django.db import models


class Filter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64)

    chat_member = models.BooleanField(default=False, help_text="Is the user a member of the channel")

    registration = models.BooleanField(default=False, help_text="Has the user registered")

    min_first_deposit = models.FloatField(null=True, blank=True)
    max_first_deposit = models.FloatField(null=True, blank=True)

    min_sum_deposits = models.FloatField(null=True, blank=True)
    max_sum_deposits = models.FloatField(null=True, blank=True)

    negative_mind = models.ForeignKey(
        "Mind", on_delete=models.SET_NULL, null=True, blank=True, related_name="negative_mind"
    )

    neutral_mind = models.ForeignKey(
        "Mind", on_delete=models.SET_NULL, null=True, blank=True, related_name="neutral_mind"
    )

    positive_mind = models.ForeignKey(
        "Mind", on_delete=models.SET_NULL, null=True, blank=True, related_name="positive_mind"
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "filter"
