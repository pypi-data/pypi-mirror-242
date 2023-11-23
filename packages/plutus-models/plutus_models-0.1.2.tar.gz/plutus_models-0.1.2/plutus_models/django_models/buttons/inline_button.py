from django.db import models


class InlineButton(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=32)
    url = models.URLField(null=True, blank=True)
    callback_data = models.CharField(max_length=64, null=True, blank=True)

    go_to_new_line = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        db_table = "inline_button"
