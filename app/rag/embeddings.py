# # app/rag/embeddings.py

# import logging
# from functools import lru_cache

# from langchain_community.embeddings import HuggingFaceEmbeddings

# logger = logging.getLogger(__name__)


# class EmbeddingService:

#     def __init__(self):

#         logger.info("🚀 Loading HuggingFace Embedding Model...")

#         self.embedding_model = HuggingFaceEmbeddings(
#             model_name="sentence-transformers/all-MiniLM-L6-v2",
#             model_kwargs={"device": "cpu"},
#             encode_kwargs={"normalize_embeddings": True}
#         )

#         logger.info("✅ Embedding model loaded successfully")

#     def embed_text(self, text: str):

#         try:
#             return self.embedding_model.embed_query(text)

#         except Exception as e:
#             logger.exception("❌ Embedding Error")
#             raise e

#     def embed_documents(self, texts: list[str]):

#         try:
#             return self.embedding_model.embed_documents(texts)

#         except Exception as e:
#             logger.exception("❌ Batch Embedding Error")
#             raise e


# @lru_cache
# def get_embedding_service():

#     return EmbeddingServi

# embedding_service = get_embedding_service()

import logging

from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


logger = logging.getLogger(__name__)


class EmbeddingService:

    def __init__(self):

        logger.info(
            "🚀 Loading HuggingFace Embedding Model..."
        )

        self.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )

        Settings.embed_model = self.embed_model

        logger.info(
            "✅ Embedding model initialized"
        )

    def get_model(self):

        return self.embed_model


embedding_service = EmbeddingService()