import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    zip_files_dir = "/tmp"
    return_zip_name = "gif-frames"
    mongo_host: str = os.environ["MONGO_HOST"]
    mongo_port: int = int(os.environ["MONGO_PORT"])
    mongo_db: str = os.environ["MONGO_DB"]
    mongo_collection: str = os.environ["MONGO_COLLECTION"]