import uuid
from django.utils.timezone import datetime, now
from app.entities.medias import Medias
from app.entities.accounts import Accounts
from app.enums.mediaTypes import MediaTypes
from django.db.models import Q
import logging

log = logging.getLogger(__name__)


class MediasRepo:
    @staticmethod
    def get_all():
        try:
            return Medias.objects.all()
        except Exception as e:
            log.error("ERROR: from get all media: " + str(e))
            return None


    @staticmethod
    def get_by_id(media_id: uuid.UUID):
        try:
            return Medias.objects.get(id=media_id)
        except Exception as e:
            log.error("ERROR: from get media by id: " + str(e))
            return None
            
    @staticmethod
    def filter_by_uploader(uploader: Accounts):
        try:
            return Medias.objects.get(uploader=uploader)
        except Exception as e:
            log.error("ERROR: from filter media by uploader: " + str(e))
            return None

    @staticmethod
    def filter_by_type(type: MediaTypes.choices):
        try:
            return Medias.objects.filter(media_type=type)
        except Exception as e:
            log.error("ERROR: from filter media by type: " + str(e))
            return None
        
    @staticmethod
    def filter_by_name(name: str):
        try:
            return Medias.objects.filter(name__icontains=name)
        except Exception as e:
            log.error("ERROR: from filter media by name: " + str(e))
            return None
        
    @staticmethod
    def filter_by_size(size: int):
        try:
            return Medias.objects.filter(size__lte=size)
        except Exception as e:
            log.error("ERROR: from filter media by size: " + str(e))
            return None
        
    @staticmethod
    def filter_by_duration(duration: int):
        try:
            return Medias.objects.filter(Q(media_type=MediaTypes.VIDEO) | Q(media_type=MediaTypes.AUDIO), duration__lte=duration)
        except Exception as e:
            log.error("ERROR: from filter media by duration: " + str(e))
            return None
        
    @staticmethod
    def filter_by_key(key: str):
        try:
            return Medias.objects.filter(key=key)
        except Exception as e:
            log.error("ERROR: from filter media by key: " + str(e))
            return None
        
    @staticmethod
    def filter_by_date_created(date: datetime):
        try:
            return Medias.objects.filter(created_at=date)
        except Exception as e:
            log.error("ERROR: from filter media by date created: " + str(e))
            return None

    @staticmethod
    def filter_by_status(status: bool = True):
        try:
            return Medias.objects.filter(is_active=status)
        except Exception as e:
            log.error("ERROR: from filter media by status: " + str(e))
            return None

    @staticmethod
    def filter_by_birth_day(date: datetime):
        try:
            return Medias.objects.filter(birth = date)
        except Exception as e:
            log.error("ERROR: from filter media by birth day: " + str(e))
            return None

    @staticmethod
    def do_create(data: dict):
        try:
            return Medias.objects.create(**data)
        except Exception as e:
            log.error("ERROR: from create media: " + str(e))
            return None

    @staticmethod
    def do_update(media: Medias, data: dict):
        try:
            for field, value in data.items():
                setattr(media, field, value)
            media.updated_at = now
            media.save(update_fields=data.keys()) 
            return media
        except Exception as e:
            log.error("ERROR: from update media: " + str(e))
            return None

    @staticmethod
    def do_delete(media: Medias):
        try:
            media.is_active = False
            media.updated_at = now
            media.save()
            return media
        except Exception as e:
            log.error("ERROR: from soft delele media: " + str(e))
            return None

    @staticmethod
    def do_hard_delete(media: Medias):
        try:
            media.delete()
            return True
        except Exception as e:
            log.error("ERROR: from hard delete media: " + str(e))
            return False
