from django.db import models

class Bitcoin(models.Model):
    market = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    eng_name = models.CharField(max_length=50)
