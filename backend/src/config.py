import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    tmp_files_dir = "/tmp"
    return_zip_name = "gif-frames"
    return_increased_framerate_gif_name = "speedup"
    return_reverted_gif_name = "reverse"
    global_metadata_key = "global_stats"
    mongo_host: str = os.environ["MONGO_HOST"]
    mongo_port: int = int(os.environ["MONGO_PORT"])
    mongo_db: str = os.environ["MONGO_DB"]
    mongo_collection: str = os.environ["MONGO_COLLECTION"]