# app/rag/text_splitter.py

"""
Production-Grade Text Splitter
------------------------------
Responsibilities:
- Split documents into semantic chunks
- Preserve context using overlap
- Optimize chunks for RAG retrieval
- Prepare chunks for embeddings

Why chunking matters:
- Better semantic retrieval
- Improved AI answers
- Reduced hallucinations
- Faster vector search
"""

import logging
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


logger = logging.getLogger(__name__)


class TextSplitterService:

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        """
        Initialize text splitter

        Recommended:
        ------------
        chunk_size:
            800 - 1500

        chunk_overlap:
            100 - 300
        """

        logger.info("🚀 Initializing Text Splitter Service")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.text_splitter = RecursiveCharacterTextSplitter(

            chunk_size=self.chunk_size,

            chunk_overlap=self.chunk_overlap,

            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ],

            length_function=len
        )

        logger.info(
            f"✅ Text Splitter Ready "
            f"(chunk_size={chunk_size}, overlap={chunk_overlap})"
        )

    def split_documents(
        self,
        documents: List[Document]
    ) -> List[Document]:
        """
        Split documents into chunks
        """

        try:

            logger.info(
                f"📄 Splitting {len(documents)} documents..."
            )

            split_docs = self.text_splitter.split_documents(
                documents
            )

            logger.info(
                f"✅ Generated {len(split_docs)} chunks"
            )

            return split_docs

        except Exception as e:

            logger.exception(
                "❌ Document splitting failed"
            )

            raise e

    def split_text(
        self,
        text: str
    ) -> List[str]:
        """
        Split raw text into chunks
        """

        try:

            logger.info("📄 Splitting raw text...")

            chunks = self.text_splitter.split_text(text)

            logger.info(
                f"✅ Generated {len(chunks)} text chunks"
            )

            return chunks

        except Exception as e:

            logger.exception(
                "❌ Text splitting failed"
            )

            raise e


# =========================================================
# SINGLETON INSTANCE
# =========================================================

text_splitter_service = TextSplitterService()


# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    sample_text = """
    Our refund policy allows customers to request
    refunds within 30 days of purchase.

    Refunds are only applicable if the product
    has not been damaged or misused.

    Customers must provide purchase proof.
    """

    splitter = TextSplitterService()

    chunks = splitter.split_text(sample_text)

    print("\n✅ Chunks Generated\n")

    for i, chunk in enumerate(chunks, start=1):

        print(f"\n--- Chunk {i} ---\n")
        print(chunk)