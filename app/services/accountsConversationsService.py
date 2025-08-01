import uuid
from typing import Dict
from django.utils.timezone import datetime, now
from app.repositories.accountsConversationsRepo import AccountsConversationsRepo
from app.services.accountsService import AccountsService
from app.services.conversationsService import ConversationsService
import logging

log = logging.getLogger(__name__)

class AccountsConversationsService:
    @staticmethod
    def find_all():
        try:
            return AccountsConversationsRepo.get_all()
        except Exception as e:
            log.error(f"ERROR: from find_all AC: {e}")
            return None

    @staticmethod
    def find_by_id(ac_id: str):
        try:
            if ac_id and str(ac_id).strip():
                uuid_obj = uuid.UUID(ac_id)
                return AccountsConversationsRepo.get_by_id(uuid_obj)
            return None
        except Exception as e:
            log.error(f"ERROR: from find_by_id AC: {e}")
            return None

    @staticmethod
    def find_by_account(account_id: str):
        try:
            if account_id and str(account_id).strip():
                account = AccountsService.find_by_id(account_id)
                if account:
                    return AccountsConversationsRepo.filter_by_account(account)
            return None
        except Exception as e:
            log.error(f"ERROR: from find_by_account AC: {e}")
            return None

    @staticmethod
    def find_by_conversation(conversation_id: str):
        try:
            if conversation_id and str(conversation_id).strip():
                conversation = ConversationsService.find_by_id(conversation_id)
                if conversation:
                    return AccountsConversationsRepo.filter_by_conversation(conversation)
            return None
        except Exception as e:
            log.error(f"ERROR: from find_by_conversation AC: {e}")
            return None

    @staticmethod
    def find_by_date_created(date: datetime = None):
        try:
            return AccountsConversationsRepo.filter_by_date_created(date or now())
        except Exception as e:
            log.error(f"ERROR: from find_by_date_created AC: {e}")
            return None

    @staticmethod
    def create(data: Dict):
        try:
            account_id = data.get("account")
            conversation_id = data.get("conversation")

            if not account_id or not conversation_id:
                return None

            account = AccountsService.find_by_id(account_id)
            conversation = ConversationsService.find_by_id(conversation_id)
            if not account or not conversation:
                log.error("ERROR: Account or Conversation not found for AC creation.")
                return None
            
            data["account"] = account
            data["conversation"] = conversation
            return AccountsConversationsRepo.do_create(data)
        except Exception as e:
            log.error(f"ERROR: from create AC: {e}")
            return None

    @staticmethod
    def update(ac_id: str, data: Dict):
        try:
            if ac_id and str(ac_id).strip() and any(data.values()):
                ac = AccountsConversationsService.find_by_id(ac_id)
                if not ac:
                    return None
                return AccountsConversationsRepo.do_update(data, ac)
            return None
        except Exception as e:
            log.error(f"ERROR: from update AC: {e}")
            return None

    @staticmethod
    def delete(ac_id: str):
        try:
            if ac_id and str(ac_id).strip():
                ac = AccountsConversationsService.find_by_id(ac_id)
                if not ac:
                    return None
                return AccountsConversationsRepo.do_delete(ac)
            return None
        except Exception as e:
            log.error(f"ERROR: from delete AC: {e}")
            return None

    @staticmethod
    def hard_delete(ac_id: str):
        try:
            if ac_id and str(ac_id).strip():
                ac = AccountsConversationsService.find_by_id(ac_id)
                if not ac:
                    return False
                return AccountsConversationsRepo.do_hard_delete(ac)
            return False
        except Exception as e:
            log.error(f"ERROR: from hard_delete AC: {e}")
            return False

    @staticmethod
    def find_common_conversation(acc1: str, acc2: str):
        try:
            ACs1 = AccountsConversationsService.find_by_account(str(acc1))
            ACs2 = AccountsConversationsService.find_by_account(str(acc2))
            if len(ACs1) != 0 and len(ACs2) != 0:
                for acc_conv1 in ACs1:
                    for acc_conv2 in ACs2:
                        if acc_conv1.get_conversation.id == acc_conv2.get_conversation.id:
                            common_conversation = ConversationsService.find_by_id(str(acc_conv1.get_conversation.id))
                            if common_conversation.is_active and not common_conversation.is_community and not common_conversation.is_group:
                                return common_conversation
            return None
        except Exception as e:
            log.error(f"ERROR: from find_common_conversation {str(e)}")
            return None
        
    @staticmethod
    def find_by_account_and_conversation(data: dict):
        try:
            return AccountsConversationsRepo.get_by_account_and_conversation(data)
        except Exception as e:
            log.error(f"ERROR: from find_common_conversation {str(e)}")
            return None