from pydantic import BaseModel
from enum import Enum

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