import os
import logging

from groq import Groq
from dotenv import load_dotenv


# =========================================================
# LOAD ENV VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# LOGGING CONFIG
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# =========================================================
# API KEY
# =========================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "❌ GROQ_API_KEY not found in .env"
    )


# =========================================================
# GROQ CLIENT
# =========================================================

client = Groq(
    api_key=GROQ_API_KEY
)


# =========================================================
# AI SERVICE
# =========================================================

class AIService:


    # =====================================================
    # SYSTEM PROMPT
    # =====================================================

    SYSTEM_PROMPT = """
You are an intelligent, professional, and helpful AI assistant
for WhatsApp conversations.

Rules:
- Give concise but useful responses.
- Be friendly and professional.
- Maintain conversation context.
- If user asks company-related questions,
  answer based on provided memory/context.
- If information is unavailable,
  honestly say you do not know.
"""


    # =====================================================
    # GENERATE AI RESPONSE
    # =====================================================

    @staticmethod
    def generate_response(
        user_message: str,
        memory: list = None
    ):
        """
        Generate contextual AI response.
        """

        try:

            if memory is None:
                memory = []

            # =============================================
            # BUILD MESSAGE HISTORY
            # =============================================

            messages = [

                {
                    "role": "system",
                    "content": AIService.SYSTEM_PROMPT
                }
            ]

            # Add conversation memory
            messages.extend(memory)

            # Add current user message
            messages.append(
                {
                    "role": "user",
                    "content": user_message
                }
            )

            # =============================================
            # CALL LLM
            # =============================================

            response = client.chat.completions.create(

                model="llama-3.3-70b-versatile",

                messages=messages,

                temperature=0.7,

                max_tokens=500,

                top_p=1,

                stream=False
            )

            ai_reply = (
                response.choices[0]
                .message
                .content
                .strip()
            )

            logger.info(
                "✅ AI response generated successfully"
            )

            return {
                "success": True,
                "response": ai_reply
            }

        except Exception as e:

            logger.error(
                f"❌ AI generation failed: {str(e)}"
            )

            return {
                "success": False,
                "response": (
                    "Sorry, I am unable to respond "
                    "right now."
                )
            }