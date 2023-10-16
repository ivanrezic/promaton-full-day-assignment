import uuid

from fastapi import FastAPI, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from utils import processing
from config import Config as cfg

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
    return {
        "total_uploads": 7,
        "total_downloads": 9,
        "total_frames": 5,
        "average_width": 442.22,
        "average_height": 323.43,
    }


@app.post("/api/upload")
async def upload_file(file: UploadFile, request: Request):
    if not file:
        raise HTTPException(status_code=400, detail="File not provided")

    # Check if the uploaded file is a GIF
    if file.content_type != "image/gif":
        raise HTTPException(status_code=400, detail="File is not a GIF")

    unique_id = uuid.uuid4()
    await processing.gif_to_frames_zip(file, unique_id)

    return {
        "url": f"{request.base_url}api/download/{unique_id}"
    }


@app.get("/api/download/{unique_id}")
async def gif_to_frames(unique_id: str):
    zip_path = f"{cfg.zip_files_dir}/{unique_id}.zip"
    return FileResponse(path=zip_path, filename=f"{cfg.return_zip_name}.zip")
