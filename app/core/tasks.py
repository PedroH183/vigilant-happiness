import io
import os
import boto3
import logging
from PIL import Image
from celery import Celery

from models.schemas import S3GetSchema, S3UploadSchema, StreamsName
from services.redis_service import RedisStreamsManager
from services.s3_service import S3BucketsImages


redis_broker = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/{os.getenv('REDIS_DB')}"

app = Celery("tasks")
app.config_from_object("celery_config")

s3_client = boto3.client("s3")
BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@app.task
def compress_image_task(image_id, filename):
    # Run into other process
    try:
        logging.info("0o0o000o0o0o0o0 Começando a compressao 0o0o000o0o0o0o0")
        logging.info(f"PARAMS : {image_id} {filename}")

        # TODO IMPLEMENTAR UMA ESTRATEGIA DE FALLBACK

        s3_client = S3BucketsImages.get_client()
        params = S3GetSchema(s3_key=f"images/{image_id}/{filename}")
        s3_obj = S3BucketsImages.get_object(s3_client, params)

        logging.info(f"Data from s3 :: {s3_obj}")

        original_bytes = s3_obj["Body"].read()

        img = Image.open(io.BytesIO(original_bytes))
        buf = io.BytesIO()

        # pegar o buffer da imagem original e salvar a compressão no buffer vazio
        img.save(buf, format="JPEG", quality=10)
        compressed_bytes = buf.getvalue()

        params = S3UploadSchema(
            image_id=image_id,
            content_type="image/jpeg",
            content=compressed_bytes,
            filename=f"compressed-{filename}",
        )
        S3BucketsImages.put_object(s3_client, params)

        RedisStreamsManager.get_client()
        RedisStreamsManager.publish_image(
            image_id, f"compressed-{filename}", StreamsName.COMPRESSAO
        )
        logging.info("0o0o0o0o0o0o0o0o Imagem comprimida salva 0o0o0o0o0o0o0o0o")

    except Exception as e:
        logging.error(f"Error compressing image: {e!s}")
        logging.error(f"Traceback: {e}", exc_info=True)
