import uuid
from fastapi import UploadFile, File, APIRouter
from s3_buckets_images_manager import S3BucketsImages, S3UploadSchema
from schemas import ErrorResponse, ImageUploadResponse, StatusEnum

router = APIRouter(tags=["Streams Manager"])

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

        # Generate a unique ID for the image
        image_id = str(uuid.uuid4())

        # Upload to S3
        s3_client = S3BucketsImages.get_client()
        upload_object_params = S3UploadSchema(
            content     = content,
            content_type= data.content_type,
            filename    = data.filename,
            image_id    = image_id
        )
        result = S3BucketsImages.put_object(s3_client, upload_object_params)

        return ImageUploadResponse(
            image_id= image_id,
            status  = StatusEnum.SUCCESS,
            message = "Image uploaded successfully",
        )
    except Exception as e:
        return ErrorResponse(
            message = str(e),
            status  = StatusEnum.ERROR,
        )


@router.get("/image/{image_id}")
async def image(image_id: str):

    # TODO: CREATE AN LOGIC TO SEND IMAGE IF IS COMPRESSED

    return {"status": "Image endpoint ready"}
