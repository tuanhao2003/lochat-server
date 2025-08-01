import uuid
from django.db import models
from django.utils.timezone import now

class Accounts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    nickname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    avatar_url = models.TextField(null=True)
    bio = models.TextField(null=True)
    birth = models.DateField(null=True)
    # public_key = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = "app"