from django.db import models


class ReplyButton(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=32)
    go_to_new_line = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        db_table = "reply_button"
