import os
import logging
from redis import Redis
from typing import Dict, List, Optional, Tuple, Union

from schemas import StreamsName


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class RedisStreamsManager:
    _instance: Optional[Redis] = None

    @classmethod
    def get_client(cls) -> Redis:
        if cls._instance is None:
            cls._instance = Redis(
                decode_responses=True,
                db=int(os.getenv("REDIS_DB", 0)),
                port=int(os.getenv("REDIS_PORT", 6379)),
                password=os.getenv("REDIS_PASSWORD", None),
                host=os.getenv("REDIS_HOST", "localhost"),
            )
        return cls._instance

    @classmethod
    def publish_image(
        cls, image_id: str, filename: Union[str, None], stream_name: str
    ) -> bool:

        try:
            client = cls.get_client()
            client.xadd(
                stream_name,
                {
                    "image_id": image_id,
                    "filename": filename or f"{image_id}-no-filename",
                },
            )
            return True
        except Exception as e:
            print(f"Error publishing to Redis: {str(e)}")
            return False

    @classmethod
    def __search_image_json(cls, image_id: str, stream_name: StreamsName):

        client = cls.get_client()

        stream_data: List[List[Tuple[str, List[Tuple[str, Dict]]]]] = client.xread(
            {stream_name: "0"}
        )  # type: ignore

        if not stream_data:
            return None
        data_access_compress: List[Tuple[str, Dict]] = stream_data[0][1]  # type: ignore

        for _, data in data_access_compress:
            logging.info(f"Serch data :: {stream_name} data :: {data}")
            if data.get("image_id") == image_id:
                return {
                    "image_id": data["image_id"],
                    "filename": data["filename"],
                }

    @classmethod
    def get_image_json(cls, image_id: str) -> Optional[dict]:

        _ = cls.get_client()

        # Verify if is completed compress
        json_obj = cls.__search_image_json(image_id, StreamsName.COMPRESSAO)

        if json_obj:
            json_obj["status"] = StreamsName.COMPRESSAO
            return json_obj

        # Verify is pending
        json_obj = cls.__search_image_json(image_id, StreamsName.UPLOAD)

        if json_obj:
            json_obj["status"] = StreamsName.UPLOAD
            return json_obj

        return None
