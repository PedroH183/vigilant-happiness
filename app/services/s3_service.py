import os
import boto3
from dotenv import load_dotenv
from models.schemas import S3GetSchema, S3UploadSchema

# Load environment variables
load_dotenv()

class S3BucketsImages:
    """Manager for S3 Buckets operations"""

    _instance = None

    @classmethod
    def get_client(cls):
        if cls._instance is None:
            cls._instance = boto3.client(
                "s3",
                region_name=os.getenv("AWS_REGION"),
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            )
        return cls._instance

    @classmethod
    def put_object(cls, s3_client, params: S3UploadSchema):

        s3_client.put_object(
            Body=params.content,
            ContentType=params.content_type,
            Bucket=os.getenv("AWS_BUCKET_NAME"),
            Key=f"images/{params.image_id}/{params.filename}",
        )
        return True

    @classmethod
    def get_object(cls, s3_client, params: S3GetSchema):

        return s3_client.get_object(
            Bucket=os.getenv("AWS_BUCKET_NAME"), 
            Key=params.s3_key
        )
