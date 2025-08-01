from django.db import models

class MessageTypes(models.TextChoices):
    TEXT = 'text', 'Text'
    MEDIA = 'media', 'Media'