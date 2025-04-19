import os
from dotenv import load_dotenv
from fastapi import FastAPI
from api.image_api import router as image_router

load_dotenv(os.path.join(os.path.dirname(__file__), "../config/.env"))

app = FastAPI(
    title="Image Compressor API",
    description="API for uploading, compressing and retrieving images",
    version="1.0.0"
)
app.include_router(image_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
