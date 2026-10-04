# app/handlers/message_handler.py

"""
Production-Grade WhatsApp Message Handler
-----------------------------------------
Responsibilities:
- Process incoming WhatsApp messages
- Validate payloads
- Handle AI conversations
- Integrate RAG pipeline
- Save conversations
- Send WhatsApp responses
- Enterprise orchestration layer
"""
from app.database.session import SessionLocal
import logging
from typing import Dict, Any, Optional

from app.rag.rag_service import (
    rag_service
)

from app.services.whatsapp_service import (
    whatsapp_service
)

from app.services.user_services import (
    user_service
)

from app.services.conversation_service import (
    conversation_service
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
# MESSAGE HANDLER
# =========================================================

class MessageHandler:

    def __init__(self):

        logger.info(
            "🚀 Initializing Message Handler"
        )

    # =====================================================
    # MAIN ENTRY
    # =====================================================

    async def process_message(
        self,
        webhook_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Main WhatsApp message processor


        """
        db=SessionLocal()

        try:

            logger.info(
                "📩 Processing incoming WhatsApp message"
            )

            # =============================================
            # EXTRACT MESSAGE
            # =============================================

            extracted_data = (
                self._extract_message_data(
                    webhook_data
                )
            )

            if not extracted_data["success"]:

                return extracted_data

            phone_number = extracted_data["phone_number"]

            user_message = extracted_data["message"]

            user_name = extracted_data["user_name" ]

            logger.info(f"👤 User: {phone_number}")

            logger.info(f"💬 Message: {user_message}")

            #db = SessionLocal()

            # =============================================
            # CREATE / GET USER
            # =============================================

            try:

                user=user_service.get_or_create_user(
                    phone_number=phone_number,
                    name=user_name,
                    db = db
                )
                # memory_messages = (conversation_service.get_recent_conversations(db=db,user_id=user.id,limit=6 ))
                # conversation_history = ""

                # for msg in memory_messages:
                #     conversation_history += (f"{msg.role}: {msg.message}\n")

            except Exception as e:

                logger.error(f"❌ User service error: "f"{str(e)}")
                return{ 
                    "success":False,"error":"User creation failed"
                }
            # load memory

            conversation_history = ""
            try:
                memory_messages = (conversation_service.get_recent_conversations(db=db,user_id=user.id,limit=6 ))
                

                for msg in memory_messages:
                    conversation_history += (f"{msg.role}: {msg.message}\n") 
            except Exception as e: 
                logger.error( f"❌ Memory load failed: {str(e)}")

            # =============================================
            # SAVE USER MESSAGE
            # =============================================

            try:

                conversation_service.save_message(
                                                    db=db,
                                                    user_id=user.id,
                                                    role="user",
                                                    message=user_message)

            except Exception as conversation_error:

                logger.error(
                    f"❌ Conversation save failed: "
                    f"{str(conversation_error)}"
                )

            # =============================================
            # HANDLE SPECIAL COMMANDS
            # =============================================

            command_response = (
                self._handle_commands(
                    user_message
                )
            )

            if command_response:

                ai_response = command_response

            else:

                # =========================================
                # GENERATE AI RESPONSE
                # =========================================
                try:
                    rag_result = (
                    rag_service.generate_response(
                        user_query=user_message,
                        memory=conversation_history

                    )
                )
                

                    if rag_result["success"]:
                        ai_response = (
                       rag_result['response']
                    )

                    else:
                        ai_response = (
                        "Sorry, I could not process "
                        "your request right now."
                    )
                except Exception as e:
                    logger.info(f"🤖 Rag error{str(e)}")
                    ai_response=("Sorry some thing went wrong")
            logger.info("Ai responce generated")

            # =============================================
            # SAVE AI RESPONSE
            # =============================================

            try:
                # ai_response = rag_result["response"]

                conversation_service.save_message(db=db,user_id=user.id,role="assistant",message=ai_response
                                                  )

            except Exception as save_error:

                logger.error(
                    f"❌ Failed to save AI response: "
                    f"{str(save_error)}"
                )

            # =============================================
            # SEND WHATSAPP MESSAGE
            # =============================================

            send_result = (
                whatsapp_service.send_text_message(

                   to_phone_number=phone_number,

                    message=ai_response
                )
            )

            logger.info(
                "✅ WhatsApp reply sent"
            )

            return {

                "success": True,

                "phone_number": phone_number,

                "user_message": user_message,

                "ai_response": ai_response,

                "whatsapp_response": send_result
            }

        except Exception as e:

            logger.exception(
                "❌ Message processing failed"
            )

            return {

                "success": False,

                "error": str(e)
            }
        finally:
                db.close()
    

    # =====================================================
    # EXTRACT WHATSAPP PAYLOAD
    # =====================================================
    

    def _extract_message_data(
        self,
        webhook_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract incoming WhatsApp message
        """

        try:

            entry = webhook_data[
                "entry"
            ][0]

            changes = entry[
                "changes"
            ][0]

            value = changes[
                "value"
            ]

            messages = value.get(
                "messages",
                []
            )

            if not messages:

                return {

                    "success": False,

                    "error": "No messages found"
                }

            message_data = messages[0]

            phone_number = (
                message_data["from"]
            )

            message_type = (
                message_data["type"]
            )

            if message_type != "text":

                return {

                    "success": False,

                    "error": (
                        "Only text messages "
                        "are supported"
                    )
                }

            user_message = (
                message_data["text"]["body"]
            )

            contacts = value.get(
                "contacts",
                []
            )

            user_name = "User"

            if contacts:

                user_name = (
                    contacts[0]
                    .get("profile", {})
                    .get("name", "User")
                )

            return {

                "success": True,

                "phone_number": phone_number,

                "message": user_message,

                "user_name": user_name
            }

        except Exception as e:

            logger.exception(
                "❌ Failed to extract message data"
            )

            return {

                "success": False,

                "error": str(e)
            }

    # =====================================================
    # COMMAND HANDLER
    # =====================================================

    def _handle_commands(
        self,
        message: str
    ) -> Optional[str]:
        """
        Handle system commands
        """

        normalized = (
            message.lower().strip()
        )

        commands = {

            "hi":
                "Hello 👋 How can I help you today?",

            "hello":
                "Hello 👋 How can I help you today?",

            "help":
                (
                    "You can ask questions about:\n"
                    "- Company policies\n"
                    "- Refunds\n"
                    "- Leave policy\n"
                    "- Services\n"
                    "- Pricing\n"
                    "- Support"
                ),

            "human":
                (
                    "A human support agent "
                    "will contact you shortly."
                ),

            "agent":
                (
                    "Connecting you to "
                    "human support."
                )
        }

        return commands.get(normalized)

    # =====================================================
    # HEALTH CHECK
    # =====================================================

    def health_check(self):

        return {

            "status": "healthy",

            "service": "message_handler"
        }


# =========================================================
# SINGLETON INSTANCE
# =========================================================

message_handler = MessageHandler()


# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    sample_payload = {

        "entry": [

            {

                "changes": [

                    {

                        "value": {

                            "messages": [

                                {

                                    "from": "919999999999",

                                    "type": "text",

                                    "text": {

                                        "body":
                                        "What is refund policy?"
                                    }
                                }
                            ],

                            "contacts": [

                                {

                                    "profile": {

                                        "name":
                                        "Rakesh"
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }

    import asyncio

    result = asyncio.run(

        message_handler.process_message(
            sample_payload
        )
    )

    print(result)