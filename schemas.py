from pydantic import BaseModel
from enum import Enum

class StatusEnum(str, Enum):
    SUCCESS = "success"
    ERROR = "error"

class ImageUploadResponse(BaseModel):
    status: StatusEnum
    message: str
    image_id: str

class ErrorResponse(BaseModel):
    status: StatusEnum
    message: str