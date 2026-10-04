import os
import logging

from dotenv import load_dotenv

from llama_index.vector_stores.postgres import PGVectorStore


# =========================================================
# LOAD ENV VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# =========================================================
# DATABASE CONFIGDB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD")
# =========================================================

DB_HOST = os.getenv("SUPABASE_DB_HOST")
DB_PORT = os.getenv("SUPABASE_DB_PORT")
DB_NAME = os.getenv("SUPABASE_DB_NAME")
DB_USER = os.getenv("SUPABASE_DB_USER")
DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD")


# =========================================================
# VALIDATION
# =========================================================

required_envs = [
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
]

if not all(required_envs):

    raise ValueError(
        "❌ Missing Supabase database environment variables"
    )


# =========================================================
# VECTOR STORE CLASS
# =========================================================

class VectorStoreManager:

    _vector_store = None

    @classmethod
    def get_vector_store(cls):
        """
        Initialize and return PGVector store.
        Singleton pattern.
        """

        try:

            if cls._vector_store is None:

                logger.info(
                    "🚀 Initializing PGVector store..."
                )

                cls._vector_store = PGVectorStore.from_params(

                    host=DB_HOST,

                    port=int(DB_PORT),

                    database=DB_NAME,

                    user=DB_USER,

                    password=DB_PASSWORD,

                    table_name="company_knowledge_base",

                    embed_dim=384,

                    hnsw_kwargs={
                        "hnsw_m": 16,
                        "hnsw_ef_construction": 64,
                        "hnsw_ef_search": 40,
                        "hnsw_dist_method": "cosine"
                    }
                )

                logger.info(
                    "✅ PGVector store initialized successfully"
                )

            return cls._vector_store

        except Exception as e:

            logger.error(
                f"❌ Vector store initialization failed: {str(e)}"
            )

            raise


# =========================================================
# HEALTH CHECK
# =========================================================

def test_vector_store_connection():
    """
    Test vector database connection.
    """

    try:

        vector_store = (
            VectorStoreManager.get_vector_store()
        )

        logger.info(
            "✅ PGVector connection successful"
        )

        return True

    except Exception as e:

        logger.error(
            f"❌ PGVector connection failed: {str(e)}"
        )

        return False