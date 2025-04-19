from dotenv import load_dotenv
import os

load_dotenv()

broker_url = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/{os.getenv('REDIS_DB')}"
result_backend = broker_url

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
enable_utc = True