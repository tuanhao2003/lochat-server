import uuid
from django.utils.timezone import datetime, now
from app.entities.conversations import Conversations
from app.entities.accounts import Accounts
import logging

log = logging.getLogger(__name__)


class ConversationsRepo:
    @staticmethod
    def get_all():
        try:
            return Conversations.objects.all()
        except Exception as e:
            log.error("ERROR: from get all conversation: " + str(e))
            return None


    @staticmethod
    def get_by_id(conversation_id: uuid.UUID):
        try:
            return Conversations.objects.get(id=conversation_id)
        except Exception as e:
            log.error("ERROR: from get conversation by id: " + str(e))
            return None
        
    @staticmethod
    def filter_by_title(title: str):
        try:
            return Conversations.objects.filter(title__icontains=title)
        except Exception as e:
            log.error("ERROR: from filter conversation by title: " + str(e))
            return None

    @staticmethod
    def get_all_personal_chats():
        try:
            return Conversations.objects.filter(is_group=False, is_community=False)
        except Exception as e:
            log.error("ERROR: from get conversation by is_group: " + str(e))
            return None
        
    @staticmethod
    def get_all_groups(isgroup: bool):
        try:
            return Conversations.objects.filter(is_group=isgroup)
        except Exception as e:
            log.error("ERROR: from get conversation by is_group: " + str(e))
            return None
        
    @staticmethod
    def get_all_communities(iscommunity: bool):
        try:
            return Conversations.objects.filter(is_community=iscommunity)
        except Exception as e:
            log.error("ERROR: from get conversation by is_community: " + str(e))
            return None
            
    @staticmethod
    def get_by_creator(creator: Accounts):
        try:
            return Conversations.objects.get(creator=creator)
        except Exception as e:
            log.error("ERROR: from get conversation by creator: " + str(e))
            return None

    @staticmethod
    def filter_by_date_created(date: datetime):
        try:
            return Conversations.objects.filter(created_at=date)
        except Exception as e:
            log.error("ERROR: from filter conversation by date created: " + str(e))
            return None

    @staticmethod
    def filter_by_status(status: bool = True):
        try:
            return Conversations.objects.filter(is_active=status)
        except Exception as e:
            log.error("ERROR: from filter conversation by status: " + str(e))
            return None

    @staticmethod
    def filter_by_birth_day(date: datetime):
        try:
            return Conversations.objects.filter(birth = date)
        except Exception as e:
            log.error("ERROR: from filter conversation by birth day: " + str(e))
            return None

    @staticmethod
    def do_create(data: dict):
        try:
            return Conversations.objects.create(**data)
        except Exception as e:
            log.error("ERROR: from create conversation: " + str(e))
            return None

    @staticmethod
    def do_update(conversation: Conversations, data: dict):
        try:
            for field, value in data.items():
                setattr(conversation, field, value)
            conversation.updated_at = now
            conversation.save(update_fields=data.keys()) 
            return conversation
        except Exception as e:
            log.error("ERROR: from update conversation: " + str(e))
            return None

    @staticmethod
    def do_delete(conversation: Conversations):
        try:
            conversation.is_active = False
            conversation.updated_at = now
            conversation.save()
            return conversation
        except Exception as e:
            log.error("ERROR: from soft delele conversation: " + str(e))
            return None

    @staticmethod
    def do_hard_delete(conversation: Conversations):
        try:
            conversation.delete()
            return True
        except Exception as e:
            log.error("ERROR: from hard delete conversation: " + str(e))
            return False
