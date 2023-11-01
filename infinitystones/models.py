from django.contrib.auth.models import User
from django.db import models


class Stone(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Activation(models.Model):
    STATUS_CHOICES = [
        ("S", "SUCCESS"),
        ("F", "FAILED"),
        ("A", "ACTIVE"),
        ("B", "NEW_ENTRY")
    ]

    id = models.BigAutoField(primary_key=True)
    stone_id = models.ForeignKey(Stone, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    start_time = models.DateTimeField(default=None)
    end_time = models.DateTimeField(default=None)
    duration = models.IntegerField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
