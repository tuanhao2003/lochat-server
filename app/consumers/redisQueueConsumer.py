import threading
import json
import time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from app.utils.redisClient import RedisClient
from app.services.messagesService import MessagesService

import logging

log = logging.getLogger(__name__)

class RedisQueueConsumer(threading.Thread):
    def __init__(self, queue_key='message_queue'):
        super().__init__(daemon=True)
        self.queue_key = queue_key
        self.running = True
        self.redis = RedisClient.instance().client

    def run(self):
        log.error(f"DEBUG: thread redis đã chạy")
        while self.running:
            try:
                result = self.redis.blpop(self.queue_key, timeout=5)
                if result:
                    _, data_str = result
                    data = json.loads(data_str)
                    self.text_message_handler(data)
            except Exception as e:
                log.error(f"DEBUG: lỗi run thread redis {str(e)}")
                time.sleep(1)

    def text_message_handler(self, data):
        try:
            result = MessagesService.create(data)
            if result:
                log.error(f"DEBUG: đã xử lý message {str(result.id)}")
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    str(result.conversation.id),
                    {
                        "type": "text",
                        "message": str(result.content),
                        "sender": str(result.sender_relation.get_account.nickname),
                        "reply_to": str(result.reply_to) if result.reply_to else None,
                    },
                )
            else:
                log.error(f"DEBUG: xử lý fail")
        except Exception as e:
            log.error(f"DEBUG: lỗi handle thread redis {str(e)}")

    def stop(self):
        self.running = False