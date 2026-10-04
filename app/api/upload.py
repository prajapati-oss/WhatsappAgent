# app/api/upload.py

"""
Production-Grade Document Upload API
------------------------------------
Responsibilities:
- Upload company documents
- Validate files
- Save uploaded files
- Trigger RAG ingestion pipeline
- Store vectors automatically

Supported:
- PDF
- DOCX
- TXT
"""

import os
import shutil
import logging
from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from app.rag.ingest_service import (
    ingestion_service
)

logger = logging.getLogger(__name__)

router = APIRouter()


# =========================================================
# CONFIG
# =========================================================

UPLOAD_DIR = "uploads"

SUPPORTED_EXTENSIONS = [
    ".pdf",
    ".docx",
    ".txt"
]

MAX_FILE_SIZE = 20 * 1024 * 1024
# 20 MB


# =========================================================
# CREATE UPLOAD DIRECTORY
# =========================================================

Path(UPLOAD_DIR).mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# DOCUMENT UPLOAD API
# =========================================================

@router.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...)
):

    try:

        logger.info(
            f"📤 Upload request received: {file.filename}"
        )

        # =================================================
        # VALIDATE FILE NAME
        # =================================================

        if not file.filename:

            raise HTTPException(
                status_code=400,
                detail="File name missing"
            )

        extension = (
            Path(file.filename)
            .suffix
            .lower()
        )

        # =================================================
        # VALIDATE FILE TYPE
        # =================================================

        if extension not in SUPPORTED_EXTENSIONS:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Unsupported file type. "
                    "Allowed: PDF, DOCX, TXT"
                )
            )

        # =================================================
        # SAVE FILE
        # =================================================

        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        logger.info(
            f"✅ File saved: {file_path}"
        )

        # =================================================
        # VALIDATE FILE SIZE
        # =================================================

        file_size = os.path.getsize(file_path)

        if file_size > MAX_FILE_SIZE:

            os.remove(file_path)

            raise HTTPException(
                status_code=400,
                detail="File too large"
            )

        # =================================================
        # START INGESTION
        # =================================================

        logger.info(
            "🚀 Starting document ingestion..."
        )

        result = (
            ingestion_service.ingest_document(
                file_path
            )
        )

        if not result["success"]:

            raise HTTPException(
                status_code=500,
                detail=result["error"]
            )

        logger.info(
            "✅ Document ingestion completed"
        )

        return {

            "success": True,

            "message": (
                "Document uploaded and "
                "indexed successfully"
            ),

            "file_name": file.filename,

            "chunks_created": result[
                "total_chunks"
            ]
        }

    except HTTPException:
        raise

    except Exception as e:

        logger.exception(
            "❌ Upload failed"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )