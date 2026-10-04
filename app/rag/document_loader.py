# app/rag/document_loader.py

"""
Production-Grade Document Loader
--------------------------------
Supports:
- PDF
- DOCX
- TXT

Responsibilities:
- Load company documents
- Extract clean text
- Prepare for chunking
- Metadata generation
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Any

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader
)

from langchain.schema import Document

logger = logging.getLogger(__name__)


class DocumentLoaderService:

    SUPPORTED_EXTENSIONS = [
        ".pdf",
        ".docx",
        ".txt"
    ]

    def __init__(self):

        logger.info("🚀 Initializing Document Loader Service")

    def load_document(self, file_path: str) -> List[Document]:
        """
        Load a single document
        """

        try:

            path = Path(file_path)

            if not path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            extension = path.suffix.lower()

            if extension not in self.SUPPORTED_EXTENSIONS:
                raise ValueError(
                    f"Unsupported file type: {extension}"
                )

            logger.info(f"📄 Loading document: {path.name}")

            loader = self._get_loader(file_path, extension)

            documents = loader.load()

            cleaned_documents = self._clean_documents(
                documents=documents,
                source_name=path.name
            )

            logger.info(
                f"✅ Loaded {len(cleaned_documents)} document pages/chunks"
            )

            return cleaned_documents

        except Exception as e:
            logger.exception("❌ Document loading failed")
            raise e

    def load_directory(self, directory_path: str) -> List[Document]:
        """
        Load all supported documents from directory
        """

        try:

            all_documents = []

            directory = Path(directory_path)

            if not directory.exists():
                raise FileNotFoundError(
                    f"Directory not found: {directory_path}"
                )

            logger.info(f"📂 Scanning directory: {directory_path}")

            for file in directory.iterdir():

                if file.suffix.lower() in self.SUPPORTED_EXTENSIONS:

                    try:
                        docs = self.load_document(str(file))
                        all_documents.extend(docs)

                    except Exception as file_error:

                        logger.error(
                            f"❌ Failed to load {file.name}: {file_error}"
                        )

            logger.info(
                f"✅ Total documents loaded: {len(all_documents)}"
            )

            return all_documents

        except Exception as e:
            logger.exception("❌ Directory loading failed")
            raise e

    def _get_loader(self, file_path: str, extension: str):
        """
        Return appropriate loader
        """

        if extension == ".pdf":
            return PyPDFLoader(file_path)

        elif extension == ".docx":
            return Docx2txtLoader(file_path)

        elif extension == ".txt":
            return TextLoader(
                file_path,
                encoding="utf-8"
            )

        else:
            raise ValueError(
                f"No loader available for: {extension}"
            )

    def _clean_documents(
        self,
        documents: List[Document],
        source_name: str
    ) -> List[Document]:
        """
        Clean and enrich metadata
        """

        cleaned_docs = []

        for index, doc in enumerate(documents):

            cleaned_text = self._clean_text(doc.page_content)

            metadata = {
                "source": source_name,
                "page": index + 1,
                "document_type": Path(source_name).suffix.lower(),
                **doc.metadata
            }

            cleaned_docs.append(
                Document(
                    page_content=cleaned_text,
                    metadata=metadata
                )
            )

        return cleaned_docs

    def _clean_text(self, text: str) -> str:
        """
        Basic text cleaning
        """

        text = text.replace("\n", " ")
        text = text.replace("\t", " ")

        text = " ".join(text.split())

        return text.strip()


document_loader_service = DocumentLoaderService()


if __name__ == "__main__":

    loader = DocumentLoaderService()

    docs = loader.load_document(
        "documents/company_policy.pdf"
    )

    print("\n✅ Document Loaded Successfully")
    print(f"Total Pages: {len(docs)}")

    print("\n📄 Sample Content:\n")
    print(docs[0].page_content[:500])

    print("\n📌 Metadata:\n")
    print(docs[0].metadata)