from django.db import models

# Create your models here.
class Thinclient(models.Model):
    local = models.CharField(max_length=255)
    ip = models.CharField(unique=True, max_length=255)
    sistema = models.CharField(max_length=255)