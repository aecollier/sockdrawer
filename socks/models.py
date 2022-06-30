from django.db import models

class Sock(models.Model):
    type = models.CharField(max_length=100)
    hasHole = models.BooleanField()