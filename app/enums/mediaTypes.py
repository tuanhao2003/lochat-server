from django.db import models

class MediaTypes(models.TextChoices):
    AUDIO = 'audio', 'Audio'
    PHOTO = 'photo', 'Photo'
    VIDEO = 'video', 'Video'
    GIF = 'gif', 'Gif'
    PDF = 'pdf', 'PDF'
    UNKNOW = 'unknow', 'Unknow'
