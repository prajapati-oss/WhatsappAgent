# app/rag/ingest_service.py

"""
Production-Grade RAG Ingestion Pipeline
---------------------------------------
Responsibilities:
- Load uploaded documents
- Split documents into chunks
- Generate embeddings
- Store vectors in PGVector
- Maintain metadata
- Power enterprise RAG systems
"""
from llama_index.core import (
    VectorStoreIndex,
    Settings
)

from app.rag.embeddings import embedding_service

Settings.embed_model = embedding_service.get_model()
import uuid
import logging
from typing import List

from llama_index.core import VectorStoreIndex
from llama_index.core.schema import TextNode
from llama_index.core.storage.storage_context import StorageContext

from app.rag.document_loader import (
    document_loader_service
)
from app.rag.embeddings import embedding_service
from app.rag.text_splitter import (
    text_splitter_service
)

from app.rag.vector_store import (
    VectorStoreManager
)


logger = logging.getLogger(__name__)


class IngestionService:

    def __init__(self):

        logger.info(
            "🚀 Initializing RAG Ingestion Service"
        )

        self.vector_store = (
            VectorStoreManager.get_vector_store()
        )

    def ingest_document(
        self,
        file_path: str
    ):
        """
        Complete ingestion pipeline

        Steps:
        ------
        1. Load document
        2. Split into chunks
        3. Convert into nodes
        4. Store vectors in PGVector
        """

        try:

            logger.info(
                f"📄 Starting ingestion: {file_path}"
            )

            # =================================================
            # LOAD DOCUMENT
            # =================================================

            documents = (
                document_loader_service.load_document(
                    file_path
                )
            )

            logger.info(
                f"✅ Loaded {len(documents)} documents"
            )

            # =================================================
            # SPLIT DOCUMENTS
            # =================================================

            split_docs = (
                text_splitter_service.split_documents(
                    documents
                )
            )

            logger.info(
                f"✅ Generated {len(split_docs)} chunks"
            )

            # =================================================
            # CONVERT TO LLAMAINDEX NODES
            # =================================================

            nodes = []

            for doc in split_docs:

                node = TextNode(

                    id_=str(uuid.uuid4()),

                    text=doc.page_content,

                    metadata=doc.metadata
                )

                nodes.append(node)

            logger.info(
                f"✅ Created {len(nodes)} vector nodes"
            )

            # =================================================
            # STORAGE CONTEXT
            # =================================================

            storage_context = StorageContext.from_defaults(
                vector_store=self.vector_store
            )

            # =================================================
            # STORE IN VECTOR DATABASE
            # =================================================

            VectorStoreIndex(
    nodes=nodes,
    storage_context=storage_context,
    embed_model=embedding_service.get_model()
)

            logger.info(
                "✅ Document successfully stored in PGVector"
            )

            return {
                "success": True,
                "total_chunks": len(nodes),
                "file_path": file_path
            }

        except Exception as e:

            logger.exception(
                "❌ Document ingestion failed"
            )

            return {
                "success": False,
                "error": str(e)
            }

    def ingest_directory(
        self,
        directory_path: str
    ):
        """
        Ingest all documents from directory
        """

        try:

            logger.info(
                f"📂 Starting directory ingestion: "
                f"{directory_path}"
            )

            documents = (
                document_loader_service.load_directory(
                    directory_path
                )
            )

            split_docs = (
                text_splitter_service.split_documents(
                    documents
                )
            )

            nodes = []

            for doc in split_docs:

                node = TextNode(

                    id_=str(uuid.uuid4()),

                    text=doc.page_content,

                    metadata=doc.metadata
                )

                nodes.append(node)

            storage_context = StorageContext.from_defaults(
                vector_store=self.vector_store
            )

            VectorStoreIndex(

                nodes=nodes,

                storage_context=storage_context
            )

            logger.info(
                "✅ Directory ingestion completed"
            )

            return {
                "success": True,
                "documents_loaded": len(documents),
                "chunks_created": len(nodes)
            }

        except Exception as e:

            logger.exception(
                "❌ Directory ingestion failed"
            )

            return {
                "success": False,
                "error": str(e)
            }


# =========================================================
# SINGLETON INSTANCE
# =========================================================

ingestion_service = IngestionService()


# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    result = ingestion_service.ingest_document(
        "documents/company_policy.pdf"
    )

    print("\n🚀 INGEST RESULT\n")

    print(result)