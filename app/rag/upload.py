from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

import os
import shutil
import uuid

from app.rag.ingest_service import (
    ingestion_service
)

router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...)
):

    try:

        # ============================================
        # GENERATE UNIQUE FILE NAME
        # ============================================

        file_extension = (
            file.filename.split(".")[-1]
        )

        unique_filename = (
            f"{uuid.uuid4()}.{file_extension}"
        )

        file_path = os.path.join(
            UPLOAD_DIR,
            unique_filename
        )

        # ============================================
        # SAVE FILE
        # ============================================

        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # ============================================
        # INGEST DOCUMENT
        # ============================================

        result = (
            ingestion_service.ingest_document(
                file_path=file_path
            )
        )

        if not result["success"]:

            raise HTTPException(
                status_code=500,
                detail=result["error"]
            )

        return {

            "success": True,

            "message":
                "Document uploaded and indexed successfully",

            "file_name": file.filename,

            "chunks_created":
                result["total_chunks"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )