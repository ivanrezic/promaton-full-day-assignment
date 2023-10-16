import os
import zipfile
from io import BytesIO
from uuid import UUID

from PIL import Image, ImageSequence

from config import Config as cfg


def gif_to_frames_zip(gif: Image, unique_id: UUID) -> None:
    os.makedirs(os.path.dirname(cfg.tmp_files_dir), exist_ok=True)
    zip_path = f"{cfg.tmp_files_dir}/{unique_id}.zip"

    with zipfile.ZipFile(zip_path, "w") as zip:
        for i in range(gif.n_frames):
            gif.seek(i)

            frame_data = BytesIO()
            gif.save(frame_data, format="PNG")

            frame_filename = f"frame_{i}.png"
            zip.writestr(frame_filename, frame_data.getvalue())


def increase_framerate(gif: Image, output_path: str, factor: float):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]
    new_duration = int(gif.info['duration'] / factor)

    frames[0].save(output_path,
                   save_all=True,
                   append_images=frames[1:],
                   optimize=False,
                   duration=new_duration,
                   loop=0)


def reverse(gif: Image, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]
    reversed_frames = frames[::-1]

    reversed_frames[0].save(output_path,
                            save_all=True,
                            append_images=reversed_frames[1:],
                            optimize=False,
                            loop=0)
