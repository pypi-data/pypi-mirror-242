from django.db import models


class Var(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    var = models.CharField(max_length=64)
    value = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.var, self.value)

    class Meta:
        db_table = "var"
