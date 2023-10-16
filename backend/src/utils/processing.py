import os
import uuid
import zipfile
from io import BytesIO
from uuid import UUID

from PIL import Image
from fastapi import UploadFile

from config import Config as cfg

from database.base_db_manager import DBManager


async def gif_to_frames_zip(file: UploadFile, unique_id: UUID) -> None:
    gif = Image.open(BytesIO(await file.read()))

    os.makedirs(os.path.dirname(cfg.zip_files_dir), exist_ok=True)
    zip_path = f"{cfg.zip_files_dir}/{unique_id}.zip"

    with zipfile.ZipFile(zip_path, "w") as zip:
        for i in range(gif.n_frames):
            gif.seek(i)

            frame_data = BytesIO()
            gif.save(frame_data, format="PNG")

            frame_filename = f"frame_{i}.png"
            zip.writestr(frame_filename, frame_data.getvalue())

def write_to_db(file: UploadFile, db_manager: DBManager) -> None:
    """TODO"""