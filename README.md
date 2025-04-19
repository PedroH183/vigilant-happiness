# Image Compressor Service

A scalable microservice for compressing and efficiently managing images using AWS S3, Redis Streams, and Celery.

## 🚀 Features

- Image upload and compression
- Asynchronous processing with Celery
- Event streaming with Redis
- Cloud storage with AWS S3
- RESTful API with FastAPI

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) | Main programming language |
| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) | API framework |
| ![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white) | Event streaming |
| ![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white) | Task queue |
| ![AWS S3](https://img.shields.io/badge/AWS_S3-569A31?style=for-the-badge&logo=amazon-aws&logoColor=white) | Cloud storage |
| ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) | Containerization |

## 📋 Requirements

- Python 3.8+
- Docker and Docker Compose
- AWS Account with S3 access
- Redis Server

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ImageCompressor.git
cd ImageCompressor
```

2. Create and configure .env file:
```properties
AWS_REGION=your-region
AWS_BUCKET_NAME=your-bucket
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
```

3. Build and run with Docker Compose:
```bash
docker-compose up --build
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | \`/image_upload\` | Upload new image |
| GET | \`/image/{image_id}\` | Get compressed image |
| GET | \`/images/list_indexs\` | List all images |

## 🔄 Process Flow

1. Client uploads image via API
2. Image is stored in S3
3. Compression task is queued in Celery
4. Redis streams track processing status
5. Compressed image is stored back in S3
6. Client can download compressed image

## 🐳 Docker Services

- \`api\`: FastAPI application
- \`worker\`: Celery worker
- \`redis\`: Redis server
