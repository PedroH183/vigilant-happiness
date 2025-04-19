import os
from redis import Redis
from typing import Optional

class RedisStreamsManager:
    _instance: Optional[Redis] = None

    @classmethod
    def get_client(cls) -> Redis:
        if cls._instance is None:
            cls._instance = Redis(
                decode_responses=True,
                port     =  int(os.getenv('REDIS_PORT', 6379)),
                password =  os.getenv('REDIS_PASSWORD', None),
                host     =  os.getenv('REDIS_HOST', 'localhost'),
            )
        return cls._instance

    @classmethod
    def publish_image(cls, image_id: str, filename: str) -> bool:
        try:
            client = cls.get_client()
            stream_name = os.getenv('REDIS_STREAM_NAME', 'image_stream')

            client.xadd(
                stream_name,
                {
                    'image_id': image_id,
                    'filename': filename,
                    'status': 'pending'
                }
            )
            return True
        except Exception as e:
            print(f"Error publishing to Redis: {str(e)}")
            return False