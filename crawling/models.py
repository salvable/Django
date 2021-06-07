from django.db import models


class Stork(models.Model):
    no = models.TextField
    name = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
