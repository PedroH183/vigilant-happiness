import os
import boto3
from pydantic import BaseModel
from typing import Optional, Union

class S3UploadSchema(BaseModel):
    image_id: str
    content: bytes
    filename: Union[str, None]
    content_type: Union[str, None]

class S3BucketsImages:
    """ Class responsible to connection with S3Buckets """

    _instance = None

    @classmethod
    def get_client(cls):
        if cls._instance is None:
            s3_client = boto3.client(
                's3',
                region_name          = os.getenv('AWS_REGION'),
                aws_access_key_id    = os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key= os.getenv('AWS_SECRET_ACCESS_KEY'),
            )
        return s3_client

    @classmethod
    def put_object(cls, s3_client, params: S3UploadSchema):
        s3_client.put_object(
            Body   =  params.content,
            ContentType = params.content_type,
            Bucket =  os.getenv('AWS_BUCKET_NAME'),
            Key    =  f'images/{params.image_id}/{params.filename}',
        )
        return True