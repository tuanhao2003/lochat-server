import uuid
from typing import Dict
from django.utils.timezone import datetime, now
from app.repositories.messagesRepo import MessagesRepo
from app.services.accountsConversationsService import AccountsConversationsService
from app.services.conversationsService import ConversationsService
from app.services.mediasService import MediasService
from app.enums.messageTypes import MessageTypes
import logging

log = logging.getLogger(__name__)

class MessagesService:
    @staticmethod
    def find_all():
        try:
            return MessagesRepo.get_all()
        except Exception as e:
            log.error(f"ERROR: from find_all messages: {e}")
            return None

    @staticmethod
    def find_by_id(message_id: str):
        try:
            if message_id and str(message_id).strip():
                uuid_obj = uuid.UUID(message_id)
                return MessagesRepo.get_by_id(uuid_obj)
            return None
        except Exception as e:
            log.error(f"ERROR: from find_by_id messages: {e}")
            return None

    @staticmethod
    def find_by_sender(sender_id: str):
        try:
            if sender_id and str(sender_id).strip():
                sender = AccountsConversationsService.find_by_id(sender_id)
                if sender:
                    return MessagesRepo.filter_by_sender(sender)
            return None
        except Exception as e:
            log.error(f"ERROR: from find_by_sender messages: {e}")
            return None

    @staticmethod
    def find_by_type(message_type: MessageTypes):
        try:
            if message_type in MessageTypes.values:
                return MessagesRepo.filter_by_type(message_type)
            return None
        except Exception as e:
            log.error(f"ERROR: from find_by_type messages: {e}")
            return None

    @staticmethod
    def find_by_media(media_id: str):
        try:
            if media_id and str(media_id).strip():
                media = MediasService.find_by_id(media_id)
                if media:
                    return MessagesRepo.filter_by_media(media)
            return None
        except Exception as e:
            log.error(f"ERROR: from find_by_media messages: {e}")
            return None

    @staticmethod
    def find_by_reply(reply_id: str):
        try:
            if reply_id and str(reply_id).strip():
                reply_msg = MessagesService.find_by_id(reply_id)
                if reply_msg:
                    return MessagesRepo.filter_by_reply(reply_msg)
            return None
        except Exception as e:
            log.error(f"ERROR: from find_by_reply messages: {e}")
            return None

    @staticmethod
    def find_by_date_created(date: datetime = None):
        try:
            return MessagesRepo.filter_by_date_created(date or now())
        except Exception as e:
            log.error(f"ERROR: from find_by_date_created messages: {e}")
            return None

    @staticmethod
    def find_by_status(status: bool = True):
        try:
            return MessagesRepo.filter_by_status(status)
        except Exception as e:
            log.error(f"ERROR: from find_by_status messages: {e}")
            return None

    @staticmethod
    def create(data: Dict):
        try:
            sender_id = data.get("sender_relation_id")
            if not sender_id:
                return None

            sender = AccountsConversationsService.find_by_id(sender_id)
            if not sender:
                log.error("ERROR: sender_relation not found.")
                return None
            
            data["conversation"] = sender.get_conversation
            new_index = 0
            if len(MessagesService.find_all()) != 0:
                new_index = int(MessagesService.find_last_conversation_message(sender.get_conversation.id).index) + 1
            data["index"] = new_index
            return MessagesRepo.do_create(data)
        except Exception as e:
            log.error(f"ERROR: from create messages: {e}")
            return None

    @staticmethod
    def update(message_id: str, data: Dict):
        try:
            if message_id and str(message_id).strip() and any(data.values()):
                msg = MessagesService.find_by_id(message_id)
                if not msg:
                    return None
                return MessagesRepo.do_update(msg, data)
            return None
        except Exception as e:
            log.error(f"ERROR: from update messages: {e}")
            return None

    @staticmethod
    def delete(message_id: str):
        try:
            if message_id and str(message_id).strip():
                msg = MessagesService.find_by_id(message_id)
                if not msg:
                    return None
                return MessagesRepo.do_delete(msg)
            return None
        except Exception as e:
            log.error(f"ERROR: from delete messages: {e}")
            return None

    @staticmethod
    def hard_delete(message_id: str):
        try:
            if message_id and str(message_id).strip():
                msg = MessagesService.find_by_id(message_id)
                if not msg:
                    return False
                return MessagesRepo.do_hard_delete(msg)
            return False
        except Exception as e:
            log.error(f"ERROR: from hard_delete messages: {e}")
            return False

    @staticmethod
    def find_last_conversation_message(conversation_id: str):
        try:
            if conversation_id and str(conversation_id).strip():
                result = MessagesRepo.get_last_conversation_message(conversation_id)
                if result:
                    log.error(f"test: find_last_conversation_message {result}")
                    return result
            return None
        except Exception as e:
            log.error(f"ERROR: find_last_conversation_message {str(e)}")
            return None
        
    @staticmethod
    def find_by_conversation(data: dict):
        try:
            conversation_id = data.get("conversation_id")
            page = int(data.get("page", "1"))
            page_size = int(data.get("page_size", "20"))
            if conversation_id:
                return MessagesRepo.filter_by_conversation(conversation_id=conversation_id, page=page, page_size=page_size)
            return None
        except Exception as e:
            log.error(f"ERROR: find_conversation_message {str(e)}")
            return None