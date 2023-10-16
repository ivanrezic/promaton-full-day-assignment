from PIL import Image

from config import Config as cfg
from database.mongo_db_manager import MongoDBManager


def get_mongo_db_manager() -> MongoDBManager:
    return MongoDBManager(
        cfg.mongo_host,
        cfg.mongo_port,
        cfg.mongo_db,
        cfg.mongo_collection,
    )


def get_current_metadata(db_manager: MongoDBManager) -> dict:
    metadata = db_manager.get_document_by_key(cfg.global_metadata_key)

    if not metadata:
        metadata = {
            "total_uploads": 0,
            "total_downloads": 0,
            "total_frames": 0,
            "sum_width": 0,
            "sum_height": 0,
        }

    return metadata


def write_metadata_to_db(gif: Image, db_manager: MongoDBManager) -> None:
    number_of_frames = gif.n_frames
    gif_width, gif_height = gif.size

    db_manager.insert_by_key(
        key=cfg.global_metadata_key,
        data={
            "$inc": {
                "total_uploads": 1,
                "total_downloads": 0,
                "total_frames": number_of_frames,
                "sum_width": gif_width,
                "sum_height": gif_height
            },
        },
    )


def increase_metadata_download_count(db_manager: MongoDBManager) -> None:
    db_manager.insert_by_key(
        key=cfg.global_metadata_key,
        data={
            "$inc": {
                "total_downloads": 1,
            },
        },
    )
