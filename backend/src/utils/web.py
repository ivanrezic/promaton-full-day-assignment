from fastapi import UploadFile, HTTPException


def check_file_validity(file: UploadFile):
    if not file:
        raise HTTPException(status_code=400, detail="File not provided")

    # Check if the uploaded file is a GIF
    if file.content_type != "image/gif":
        raise HTTPException(status_code=400, detail="File is not a GIF")
