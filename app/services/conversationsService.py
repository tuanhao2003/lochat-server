import uuid
from typing import Dict
from django.utils.timezone import datetime, now
from app.repositories.conversationsRepo import ConversationsRepo
from app.services.accountsService import AccountsService
import logging

log = logging.getLogger(__name__)


class ConversationsService:
    @staticmethod
    def find_all():
        try:
            return ConversationsRepo.get_all()
        except Exception as e:
            log.error(f"ERROR: from find_all conversation: {e}")
            return None

    @staticmethod
    def find_by_id(conversation_id: str):
        try:
            if conversation_id and str(conversation_id).strip():
                uuid_obj = uuid.UUID(conversation_id)
                return ConversationsRepo.get_by_id(uuid_obj)
            return None
        except Exception as e:
            log.error(f"ERROR: from find_by_id conversation: {e}")
            return None

    @staticmethod
    def find_by_title(title: str):
        try:
            if title and str(title).strip():
                return ConversationsRepo.filter_by_title(title)
            return None
        except Exception as e:
            log.error(f"ERROR: from find_by_title conversation: {e}")
            return None

    @staticmethod
    def find_all_personal_chats():
        try:
            return ConversationsRepo.get_all_personal_chats()
        except Exception as e:
            log.error(f"ERROR: from find_all_personal_chats: {e}")
            return None

    @staticmethod
    def find_all_groups(is_group: bool = True):
        try:
            return ConversationsRepo.get_all_groups(is_group)
        except Exception as e:
            log.error(f"ERROR: from find_all_groups: {e}")
            return None

    @staticmethod
    def find_all_communities(is_community: bool = True):
        try:
            return ConversationsRepo.get_all_communities(is_community)
        except Exception as e:
            log.error(f"ERROR: from find_all_communities: {e}")
            return None

    @staticmethod
    def find_by_creator(account_id: str):
        try:
            if account_id and str(account_id).strip():
                creator = AccountsService.find_by_id(account_id)
                if creator:
                    return ConversationsRepo.get_by_creator(creator)
            return None
        except Exception as e:
            log.error(f"ERROR: from find_by_creator conversation: {e}")
            return None

    @staticmethod
    def find_by_date_created(date: datetime = None):
        try:
            return ConversationsRepo.filter_by_date_created(date or now())
        except Exception as e:
            log.error(f"ERROR: from find_by_date_created conversation: {e}")
            return None

    @staticmethod
    def find_by_birth_day(date: datetime):
        try:
            if date:
                return ConversationsRepo.filter_by_birth_day(date)
            return None
        except Exception as e:
            log.error(f"ERROR: from find_by_birth_day conversation: {e}")
            return None

    @staticmethod
    def find_by_status(status: bool = True):
        try:
            return ConversationsRepo.filter_by_status(status)
        except Exception as e:
            log.error(f"ERROR: from find_by_status conversation: {e}")
            return None

    @staticmethod
    def create(data: Dict):
        try:
            return ConversationsRepo.do_create(data)
        except Exception as e:
            log.error(f"ERROR: from create conversation: {e}")
            return None

    @staticmethod
    def update(conversation_id: str, data: Dict):
        try:
            if conversation_id and str(conversation_id).strip() and any(data.values()):
                conversation = ConversationsService.find_by_id(conversation_id)
                if not conversation:
                    return None
                return ConversationsRepo.do_update(conversation, data)
            return None
        except Exception as e:
            log.error(f"ERROR: from update conversation: {e}")
            return None

    @staticmethod
    def delete(conversation_id: str):
        try:
            if conversation_id and str(conversation_id).strip():
                conversation = ConversationsService.find_by_id(conversation_id)
                if not conversation:
                    return None
                return ConversationsRepo.do_delete(conversation)
            return None
        except Exception as e:
            log.error(f"ERROR: from delete conversation: {e}")
            return None

    @staticmethod
    def hard_delete(conversation_id: str):
        try:
            if conversation_id and str(conversation_id).strip():
                conversation = ConversationsService.find_by_id(conversation_id)
                if not conversation:
                    return False
                return ConversationsRepo.do_hard_delete(conversation)
            return False
        except Exception as e:
            log.error(f"ERROR: from hard_delete conversation: {e}")
            return False