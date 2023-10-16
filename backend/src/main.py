import uuid
from io import BytesIO

from PIL import Image
from fastapi import FastAPI, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import utils.database
from config import Config as cfg
from utils import processing, web

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/meta")
async def get_meta():
    mongo_db_manager = utils.database.get_mongo_db_manager()
    current_metadata = utils.database.get_current_metadata(mongo_db_manager)

    total_uploads = current_metadata["total_uploads"]
    avg_width = current_metadata["sum_width"] / total_uploads if total_uploads else 0
    avg_height = current_metadata["sum_height"] / total_uploads if total_uploads else 0

    return {
        "total_uploads": total_uploads,
        "total_downloads": current_metadata["total_downloads"],
        "total_frames": current_metadata["total_frames"],
        "average_width": round(avg_width, 3),
        "average_height": round(avg_height, 3),
    }


@app.post("/api/upload")
async def upload_file(file: UploadFile, request: Request):
    web.check_file_validity(file)
    gif = Image.open(BytesIO(await file.read()))

    unique_id = uuid.uuid4()
    processing.gif_to_frames_zip(gif, unique_id)

    mongo_db_manager = utils.database.get_mongo_db_manager()
    utils.database.write_metadata_to_db(gif, mongo_db_manager)

    return {
        "url": f"{request.base_url}api/download/{unique_id}",
    }


@app.get("/api/download/{unique_id}")
async def gif_to_frames(unique_id: str):
    zip_path = f"{cfg.tmp_files_dir}/{unique_id}.zip"

    mongo_db_manager = utils.database.get_mongo_db_manager()
    utils.database.increase_metadata_download_count(mongo_db_manager)

    return FileResponse(path=zip_path, filename=f"{cfg.return_zip_name}.zip")


@app.post("/api/change_rate")
async def change_rate(file: UploadFile, factor: float = 2):
    web.check_file_validity(file)
    gif = Image.open(BytesIO(await file.read()))

    unique_id = uuid.uuid4()
    output_path = f"{cfg.tmp_files_dir}/{unique_id}.gif"

    processing.increase_framerate(gif, output_path, factor=factor)
    return FileResponse(path=output_path, filename=f"{cfg.return_increased_framerate_gif_name}.gif")


@app.post("/api/reverse")
async def change_rate(file: UploadFile):
    web.check_file_validity(file)
    gif = Image.open(BytesIO(await file.read()))

    unique_id = uuid.uuid4()
    output_path = f"{cfg.tmp_files_dir}/{unique_id}.gif"

    processing.reverse(gif, output_path)
    return FileResponse(path=output_path, filename=f"{cfg.return_reverted_gif_name}.gif")
