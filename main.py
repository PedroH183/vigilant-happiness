from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="Image Server Compressor Api", 
    description="API to receive images and publish into a Redis Streams",
)
load_dotenv()


@app.get("/ping")
async def ping():
    return {"status": "OK"}

from image_compressor_api import router

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)