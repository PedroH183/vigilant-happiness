from enum import Enum
from typing import List, Union
from pydantic import BaseModel, field_validator


class StatusEnum(str, Enum):
    SUCCESS = "success"
    ERROR = "error"


class StreamsName(str, Enum):
    UPLOAD = "imagem_upload"
    COMPRESSAO = "compressao_concluida"


class ImageUploadResponse(BaseModel):
    status: StatusEnum
    message: str
    image_id: str


class ErrorResponse(BaseModel):
    status: StatusEnum
    message: str


class S3UploadSchema(BaseModel):
    image_id: str
    content: bytes
    filename: Union[str, None]
    content_type: Union[str, None]

    @field_validator("filename")
    def filename_validator(filename):
        return filename if filename else ""


class S3GetSchema(BaseModel):
    s3_key: str


class ImageIndex(BaseModel):
    image_id: str
    filename: str

class ImageIndexResponse(BaseModel):
    status: str
    indexes: List[ImageIndex]