import threading
import json
import time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from app.utils.redisClient import RedisClient
from app.services.messagesService import MessagesService
from app.enums.messageTypes import MessageTypes
from app.enums.mediaTypes import MediaTypes 
from app.services.mediasService import MediasService

import logging

log = logging.getLogger(__name__)

class RedisQueueConsumer(threading.Thread):
    def __init__(self, queue_key='message_queue'):
        super().__init__(daemon=True)
        self.queue_key = queue_key
        self.running = True
        self.redis = RedisClient.instance().client

    def run(self):
        while self.running:
            try:
                result = self.redis.blpop(self.queue_key, timeout=5)
                if result:
                    _, data_str = result
                    data = json.loads(data_str)
                    if data.get("type") == MessageTypes.TEXT:
                        self.text_message_handler(data)
                    else:
                        self.media_message_handler(data)
            except Exception as e:
                log.error(f"Redis consumer error: {e}")
                time.sleep(1)

    def text_message_handler(self, data):
        try:
            result = MessagesService.create(data)
            if result:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    str(result.conversation.id),
                    {
                        "type": data.get("type"),
                        "content": str(result.content),
                        "sender": str(result.sender_relation.get_account.nickname),
                        "reply_to": str(result.reply_to) if result.reply_to else None,
                    },
                )
            else:
                log.error(f"DEBUG: xử lý fail")
        except Exception as e:
            log.error(f"DEBUG: lỗi handle thread redis {str(e)}")

    def media_message_handler(self, data):
        try:
            media_data = {
                "uploader_id": data.get("sender_relation_id"),
                "name": data.get("media_name"),
                "type": data.get("media_type"),
                "size": data.get("media_size"),
                "url": data.get("media_url"),
            }
            media_created = MediasService.create(media_data)
            if media_created:
                data["media_id"] = media_created.id
                result = MessagesService.create(data)
                if result:
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        str(result.conversation.id),
                        {
                            "type": data.get("type"),
                            "content": str(result.content),
                            "sender": str(result.sender_relation.get_account.nickname),
                            "reply_to": str(result.reply_to) if result.reply_to else None,
                            "media_type": str(result.media.type),
                            "media_name": str(result.media.name),
                            "media_url": str(result.media.url),
                        },
                    )
                else:
                    log.error(f"DEBUG: xử lý fail")
            else:
                log.error(f"DEBUG: xử lý media fail")
        except Exception as e:
            log.error(f"DEBUG: lỗi handle thread redis {str(e)}")

    def stop(self):
        self.running = False