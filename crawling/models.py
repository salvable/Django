from django.db import models


class Stork(models.Model):
    stork_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
