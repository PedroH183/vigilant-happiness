from enum import Enum
from typing import List
from pydantic import BaseModel


class StatusEnum(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    PROCESSING = "processing"


class StreamsName(str, Enum):
    UPLOAD = "imagens_uploaded"
    COMPRESSAO = "compressao_concluida"


class S3UploadSchema(BaseModel):
    image_id: str
    filename: str
    content: bytes
    content_type: str


class S3GetSchema(BaseModel):
    s3_key: str


class ImageUploadResponse(BaseModel):
    image_id: str
    status: StatusEnum
    message: str


class ErrorResponse(BaseModel):
    status: StatusEnum
    message: str


class ImageIndex(BaseModel):
    image_id: str
    filename: str


class ImageIndexResponse(BaseModel):
    status: str
    indexes: List[ImageIndex]
