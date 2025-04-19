import io
import uuid
import logging
from typing import Optional, Dict
from tasks import compress_image_task
from fastapi.responses import StreamingResponse
from redis_streams_manager import RedisStreamsManager
from fastapi import HTTPException, UploadFile, File, APIRouter
from s3_buckets_images_manager import S3BucketsImages, S3UploadSchema
from schemas import ErrorResponse, ImageIndex, ImageIndexResponse, ImageUploadResponse, S3GetSchema, StatusEnum, StreamsName

router = APIRouter(tags=["Streams Manager"])

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@router.post("/image_upload", 
    response_model=ImageUploadResponse, 
    responses={
        200: {"model": ImageUploadResponse},
        400: {"model": ErrorResponse}
    }
)
async def image_upload(data: UploadFile = File(...)):
    try:
        content = await data.read()
        image_id = str(uuid.uuid4())

        s3_client = S3BucketsImages.get_client()
        upload_object_params = S3UploadSchema(
            content     = content,
            content_type= data.content_type,
            filename    = data.filename,
            image_id    = image_id
        )
        result = S3BucketsImages.put_object(s3_client, upload_object_params)

        if not result:
            raise ValueError("Não foi possivel fazer o upload da imagem no S3")

        RedisStreamsManager.get_client()
        RedisStreamsManager.publish_image(image_id, data.filename, StreamsName.UPLOAD)

        compress_image_task.delay(image_id, upload_object_params.filename)

        return ImageUploadResponse(
            image_id= image_id,
            status  = StatusEnum.SUCCESS,
            message = "Image uploaded successfully"
        )
    except Exception as e:
        return ErrorResponse(
            message = str(e),
            status  = StatusEnum.ERROR
        )


@router.get("/image/{image_id}")
async def get_image_binary(image_id: str):

    RedisStreamsManager.get_client()
    image_obj: Optional[Dict] = RedisStreamsManager.get_image_json(image_id) # type: ignore

    if not image_obj:
        raise HTTPException(
            status_code=404,
            detail="Image not found"
        )

    if image_obj["status"] != StreamsName.COMPRESSAO:
        return {
            "status": "processing",
            "message": "Image is still being compressed"
        }

    # If compression is complete, get from S3
    s3_client = S3BucketsImages.get_client()
    compressed_key = f"images/{image_id}/{image_obj['filename']}"

    logging.info(f"GENRATED KEY ::: {compressed_key}")

    try:
        params = S3GetSchema(s3_key=compressed_key)
        s3_response = S3BucketsImages.get_object(s3_client, params)

    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Compressed image not found: {str(e)}"
        )

    # Get image content
    image_data = s3_response['Body'].read()

    # Return streaming response
    return StreamingResponse(
        io.BytesIO(image_data),
        media_type=s3_response['ContentType'],
        headers={
            'Content-Disposition': f'attachment; filename="{image_obj["filename"]}"'
        }
    )


@router.get("/images/list_indexs", response_model=ImageIndexResponse)
async def get_images_indexs():

    images = {}
    redis_client = RedisStreamsManager.get_client()
    upload_stream = redis_client.xread({StreamsName.UPLOAD: '0'})

    if not upload_stream:
        return ImageIndexResponse(
            status="success",
            indexes=[]
        )

    if upload_stream:
        upload_stream = upload_stream # type: ignore
        for _, messages in upload_stream: # type: ignore
            for msg_id, data in messages:
                images[data['image_id']] = ImageIndex(
                    image_id=data['image_id'],
                    filename=data['filename'],
                )

    return ImageIndexResponse(
        status="success",
        indexes=list(images.values())
    )