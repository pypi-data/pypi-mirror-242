from django.db import models


class NoneObject(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "none_object"
