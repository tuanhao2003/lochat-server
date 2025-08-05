import uuid
from django.utils.timezone import datetime, now
from app.entities.messages import Messages 
from app.entities.medias import Medias 
from app.entities.accountsConversations import AccountsConversations
from app.enums.messageTypes import MessageTypes
from django.core.paginator import Paginator
import logging

log = logging.getLogger(__name__)


class MessagesRepo:
    @staticmethod
    def get_all():
        try:
            return Messages.objects.all()
        except Exception as e:
            log.error("ERROR: from get all messages: " + str(e))
            return None


    @staticmethod
    def get_by_id(message_id: uuid.UUID):
        try:
            return Messages.objects.get(id=message_id)
        except Exception as e:
            log.error("ERROR: from get message by id: " + str(e))
            return None
            
    @staticmethod
    def filter_by_sender(sender: AccountsConversations):
        try:
            return Messages.objects.filter(sender_relation=sender)
        except Exception as e:
            log.error("ERROR: from filter message by sender: " + str(e))
            return None

    @staticmethod
    def filter_by_type(type: MessageTypes.choices):
        try:
            return Messages.objects.filter(type=type)
        except Exception as e:
            log.error("ERROR: from filter message by type: " + str(e))
            return None
        
    @staticmethod
    def filter_by_media(media: Medias):
        try:
            return Messages.objects.filter(media=media)
        except Exception as e:
            log.error("ERROR: from filter message by media: " + str(e))
            return None
        
    @staticmethod
    def filter_by_reply(rep: Messages):
        try:
            return Messages.objects.filter(reply_to=rep)
        except Exception as e:
            log.error("ERROR: from filter message by reply: " + str(e))
            return None
        
    @staticmethod
    def filter_by_date_created(date: datetime):
        try:
            return Messages.objects.filter(created_at=date)
        except Exception as e:
            log.error("ERROR: from filter message by date created: " + str(e))
            return None

    @staticmethod
    def filter_by_status(status: bool = True):
        try:
            return Messages.objects.filter(is_active=status)
        except Exception as e:
            log.error("ERROR: from filter message by status: " + str(e))
            return None

    @staticmethod
    def do_create(data: dict):
        try:
            return Messages.objects.create(**data)
        except Exception as e:
            log.error("ERROR: from create message: " + str(e))
            return None

    @staticmethod
    def do_update(message: Messages, data: dict):
        try:
            for field, value in data.items():
                setattr(message, field, value)
            message.updated_at = now
            message.save(update_fields=data.keys()) 
            return message
        except Exception as e:
            log.error("ERROR: from update message: " + str(e))
            return None

    @staticmethod
    def do_delete(message: Messages):
        try:
            message.is_active = False
            message.updated_at = now
            message.save()
            return message
        except Exception as e:
            log.error("ERROR: from soft delele message: " + str(e))
            return None

    @staticmethod
    def do_hard_delete(message: Messages):
        try:
            message.delete()
            return True
        except Exception as e:
            log.error("ERROR: from hard delete message: " + str(e))
            return False

    @staticmethod
    def get_last_conversation_message(conversation_id):
        try:
            return Messages.objects.filter(conversation__id=conversation_id).order_by("-index").first()
        except Exception as e:
            log.error(f"ERROR: get_last_conversation_message {str(e)}")
            return None
        
    @staticmethod
    def filter_by_conversation(conversation_id: uuid.UUID, page: int = 1, page_size: int = 20):
        try:
            query_result = Messages.objects.filter(conversation__id=conversation_id).order_by("-index")
            paginated = Paginator(query_result, page_size)
            content = paginated.page(page)
            return {
                "pages_count": paginated.num_pages,
                "current_page": content.number,
                "page_content": list(content)
            }
        except Exception as e:
            log.error(f"ERROR: get_conversation_message {str(e)}")
            return None