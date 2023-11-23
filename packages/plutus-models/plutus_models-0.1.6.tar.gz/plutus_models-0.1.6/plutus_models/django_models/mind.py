from django.db import models


class Mind(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64)

    f_filter = models.ForeignKey("Filter", on_delete=models.SET_NULL, null=True, blank=True)

    action = models.ForeignKey("Action", on_delete=models.SET_NULL, null=True, blank=True, related_name="actions")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "mind"
