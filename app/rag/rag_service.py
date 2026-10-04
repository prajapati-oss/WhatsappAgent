# app/rag/rag_service.py

"""
Production-Grade RAG Service
----------------------------
Responsibilities:
- Retrieve relevant context
- Generate AI response using Groq
- Enterprise-grade RAG pipeline
- Context-aware responses
- Hallucination reduction
- WhatsApp AI brain
"""

import os
import logging
from typing import Dict, Any

from dotenv import load_dotenv

from groq import Groq

from app.rag.retrieval_service import (
    retrieval_service
)


# =========================================================
# LOAD ENV
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
# ENV VARIABLES
# =========================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL_NAME = os.getenv(
    "GROQ_MODEL_NAME",
    "llama-3.1-8b-instant"
)


# =========================================================
# VALIDATION
# =========================================================

if not GROQ_API_KEY:

    raise ValueError(
        "❌ Missing GROQ_API_KEY in .env"
    )


# =========================================================
# RAG SERVICE
# =========================================================

class RAGService:

    def __init__(self):

        logger.info(
            "🚀 Initializing RAG Service"
        )

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

    def generate_response(
        self,
        user_query: str,
        top_k: int = 5,
        memory:str=""
    ) -> Dict[str, Any]:
        """
        Complete RAG Pipeline

        Flow:
        -----
        User Query
            ↓
        Vector Retrieval
            ↓
        Relevant Context
            ↓
        Groq LLM
            ↓
        Final AI Response
        """

        try:

            logger.info(
                f"🤖 Processing query: {user_query}"
            )

            # =============================================
            # RETRIEVE CONTEXT
            # =============================================

            retrieval_result = (
                retrieval_service.retrieve_context(
                    query=user_query,
                    top_k=top_k
                )
            )

            if not retrieval_result["success"]:

                return {

                    "success": False,

                    "error": retrieval_result[
                        "error"
                    ]
                }

            context = retrieval_result["context"]

            system_prompt = f"""
You are an enterprise AI assistant.

Previous Conversation:
{memory}

Company Knowledge Base:
{context}

Current User Question:
{user_query}

Instructions:
- Answer professionally
- Use previous conversation context if relevant
- Answer from company knowledge base when possible
- If answer is not available, say politely that information is unavailable
"""

            # =============================================
            # SYSTEM PROMPT
            # =============================================

#             system_prompt = f"""
# You are an enterprise AI assistant.

# Your job is to answer user questions ONLY
# from the provided company knowledge base.

# RULES:
# - Answer ONLY from provided context
# - Do not hallucinate
# - If answer not found, say:
#   "I could not find that information
#    in the company knowledge base."
# - Keep answers professional
# - Keep answers concise
# - Be helpful and accurate

# COMPANY KNOWLEDGE BASE:
# {context}

# """


            # =============================================
            # GENERATE RESPONSE
            # =============================================

            response = (
                self.client.chat.completions.create(

                    model=GROQ_MODEL_NAME,

                    messages=[

                        {
                            "role": "system",
                            "content": system_prompt
                        },

                        {
                            "role": "user",
                            "content": user_query
                        }
                    ],

                    temperature=0.2,

                    max_tokens=700
                )
            )

            ai_response = (
                response.choices[0]
                .message.content
            )

            logger.info(
                "✅ AI response generated"
            )

            return {

                "success": True,

                "query": user_query,

                "response": ai_response,

                "retrieved_chunks": (
                    retrieval_result[
                        "matches_found"
                    ]
                ),

                "sources": (
                    retrieval_result[
                        "results"
                    ]
                )
            }

        except Exception as e:

            logger.exception(
                "❌ RAG generation failed"
            )

            return {

                "success": False,

                "error": str(e)
            }

    def ask(
        self,
        question: str
    ) -> str:
        """
        Simplified chat method
        """

        result = self.generate_response(
            user_query=question, 
            
        )

        if not result["success"]:

            return (
                "Sorry, something went wrong."
            )

        return result["response"]


# =========================================================
# SINGLETON INSTANCE
# =========================================================

rag_service = RAGService()


# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    query = (
        "What is the refund policy?"
    )

    result = rag_service.generate_response(
        user_query=query
    )

    print("\n🚀 RAG RESPONSE\n")

    print(result)