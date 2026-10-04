# app/rag/retrieval_service.py

"""
Production-Grade Retrieval Service
----------------------------------
Responsibilities:
- Semantic similarity search
- Retrieve relevant chunks
- Query PGVector
- Prepare context for LLM
- Enterprise RAG retrieval layer
"""

import logging
from typing import List, Dict, Any

from llama_index.core import (
    VectorStoreIndex,
    Settings
)

from llama_index.core.vector_stores.types import (
    VectorStoreQueryMode
)

from llama_index.core.retrievers import (
    VectorIndexRetriever
)

from llama_index.core.query_engine import (
    RetrieverQueryEngine
)

from llama_index.core.postprocessor import (
    SimilarityPostprocessor
)

from llama_index.core.storage.storage_context import (
    StorageContext
)

from app.rag.vector_store import (
    VectorStoreManager
)

from app.rag.embeddings import (
    embedding_service
)


# =========================================================
# GLOBAL SETTINGS
# =========================================================

Settings.embed_model = (
    embedding_service.get_model()
)


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# =========================================================
# RETRIEVAL SERVICE
# =========================================================

class RetrievalService:

    def __init__(self):

        logger.info(
            "🚀 Initializing Retrieval Service"
        )

        self.vector_store = (
            VectorStoreManager.get_vector_store()
        )

        self.index = self._initialize_index()

    def _initialize_index(self):
        """
        Initialize vector index
        """

        try:

            storage_context = (
                StorageContext.from_defaults(
                    vector_store=self.vector_store
                )
            )

            index = VectorStoreIndex.from_vector_store(
                vector_store=self.vector_store,
                storage_context=storage_context,
                embed_model=embedding_service.get_model()
            )

            logger.info(
                "✅ Vector index initialized"
            )

            return index

        except Exception as e:

            logger.exception(
                "❌ Failed to initialize vector index"
            )

            raise e

    def retrieve_context(
        self,
        query: str,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Retrieve relevant context from PGVector
        """

        try:

            logger.info(
                f"🔍 Searching context for query: {query}"
            )

            retriever = VectorIndexRetriever(

                index=self.index,

                similarity_top_k=top_k,

                vector_store_query_mode=(
                    VectorStoreQueryMode.DEFAULT
                )
            )

            nodes = retriever.retrieve(query)

            logger.info(
                f"✅ Retrieved {len(nodes)} chunks"
            )

            results = []

            combined_context = ""

            for index, node in enumerate(nodes):

                text = node.text

                metadata = node.metadata

                score = (
                    node.score
                    if hasattr(node, "score")
                    else None
                )

                result = {

                    "rank": index + 1,

                    "score": score,

                    "text": text,

                    "metadata": metadata
                }

                results.append(result)

                combined_context += (
                    f"\n\n{text}"
                )

            return {

                "success": True,

                "query": query,

                "top_k": top_k,

                "matches_found": len(results),

                "context": combined_context.strip(),

                "results": results
            }

        except Exception as e:

            logger.exception(
                "❌ Retrieval failed"
            )

            return {

                "success": False,

                "error": str(e)
            }

    def search_documents(
        self,
        query: str,
        top_k: int = 5
    ):
        """
        Simplified search API
        """

        result = self.retrieve_context(
            query=query,
            top_k=top_k
        )

        return result

    def ask(
        self,
        question: str,
        top_k: int = 5
    ):
        """
        Retrieve only context text
        Useful for RAG pipelines
        """

        result = self.retrieve_context(
            query=question,
            top_k=top_k
        )

        if not result["success"]:

            return None

        return result["context"]


# =========================================================
# SINGLETON INSTANCE
# =========================================================

retrieval_service = RetrievalService()


# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    service = RetrievalService()

    query = (
        "What is company refund policy?"
    )

    result = service.retrieve_context(
        query=query,
        top_k=3
    )

    print("\n🚀 RETRIEVAL RESULT\n")

    print(result)