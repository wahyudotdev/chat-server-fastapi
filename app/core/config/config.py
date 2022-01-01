import os
from pathlib import Path
from dotenv import load_dotenv


env_path = Path("./.env")
load_dotenv(env_path)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_URL = os.getenv("ROOT_URL", "")
API_V1_STR = ROOT_URL + os.getenv("API_V1_STR", "/api/v1")

# Generate Secret Key if it doesn't provided using command openssl rand -hex 32
SECRET_KEY=os.getenv("SECRET_KEY")

# MongoDB Config
MONGODB_HOST = os.getenv("MONGODB_HOST")
MONGODB_USER = os.getenv("MONGODB_USER")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_NAME = os.getenv("MONGODB_NAME")
MONGODB_PORT = os.getenv("MONGODB_PORT", "27017")
MONGODB_URL = f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/"

DATABASE_MODELS_DIR = os.path.join(PROJECT_DIR, "models")

if not MONGODB_USER and not MONGODB_PASSWORD:
    MONGODB_URL = (
        f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/"
    )

MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))

database_name = MONGODB_NAME

PARSER_BASE_URL = os.getenv("PARSER_BASE_URL", "http://127.0.0.1:4000/isl/api/v1")
API_BASE_URL = os.getenv('API_BASE_URL', f'http://127.0.0.1:4001{API_V1_STR}')
SCHEDULER_BASE_URL = os.getenv('SCHEDULER_BASE_URL', 'http://127.0.0.1:4002/scheduler/api/v1')