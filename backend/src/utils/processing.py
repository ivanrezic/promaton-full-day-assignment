import os
import zipfile
from io import BytesIO
from uuid import UUID

from PIL import Image, ImageSequence

from config import Config as cfg


def gif_to_frames_zip(gif: Image, unique_id: UUID) -> None:
    os.makedirs(os.path.dirname(cfg.zip_files_dir), exist_ok=True)
    zip_path = f"{cfg.zip_files_dir}/{unique_id}.zip"

    with zipfile.ZipFile(zip_path, "w") as zip:
        for i in range(gif.n_frames):
            gif.seek(i)

            frame_data = BytesIO()
            gif.save(frame_data, format="PNG")

            frame_filename = f"frame_{i}.png"
            zip.writestr(frame_filename, frame_data.getvalue())