import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database.models import Conversation

from sqlalchemy.orm import Session
from app.database.models import Conversation
# =========================================================
# LOGGING

# =========================================================

logger = logging.getLogger(__name__)


# =========================================================
# CONVERSATION SERVICE
# =========================================================

class ConversationService:


    # =====================================================
    # SAVE MESSAGE
    # =====================================================

    @staticmethod
    def save_message(
        db: Session,
        user_id: int,
        role: str,
        message: str,
        message_type: str = "text",
        whatsapp_message_id: str = None,
        sentiment: str = None
    ):
        """
        Save conversation message.
        """

        try:

            conversation = Conversation(
                user_id=user_id,
                role=role,
                message=message,
                message_type=message_type,
                whatsapp_message_id=whatsapp_message_id,
                sentiment=sentiment
            )

            db.add(conversation)

            db.commit()

            db.refresh(conversation)

            logger.info(
                f"✅ Conversation saved | "
                f"user_id={user_id} | role={role}"
            )

            return conversation

        except SQLAlchemyError as e:

            db.rollback()

            logger.error(
                f"❌ Failed to save conversation: {str(e)}"
            )

            return None


    # =====================================================
    # GET RECENT CONVERSATIONS
    # =====================================================

    @staticmethod
    def get_recent_conversations(
        db: Session,
        user_id: int,
        limit: int = 5
    ):
        """
        Fetch recent user conversations.
        """

        try:

            conversations = (
                db.query(Conversation)
                .filter(Conversation.user_id == user_id)
                .order_by(Conversation.created_at.desc())
                .limit(limit)
                .all()
            )

            # oldest → newest
            #conversations.reverse()

            logger.info(
                f"✅ Retrieved {len(conversations)} "
                f"messages for user_id={user_id}"
            )

            return list (reversed(conversations))

        except SQLAlchemyError as e:

            logger.error(
                f"❌ Failed to fetch conversations: {str(e)}"
            )

            return []
        


    # =====================================================
    # FORMAT MEMORY FOR AI
    # =====================================================

    @staticmethod
    def build_chat_memory(
        conversations
    ):
        """
        Convert DB conversations into AI-ready format.
        """

        try:

            memory = []

            for convo in conversations:

                memory.append({
                    "role": convo.role,
                    "content": convo.message
                })

            logger.info(
                f"✅ Memory built with "
                f"{len(memory)} messages"
            )

            return memory

        except Exception as e:

            logger.error(
                f"❌ Failed to build memory: {str(e)}"
            )

            return []


    # =====================================================
    # DELETE USER CONVERSATIONS
    # =====================================================

    @staticmethod
    def delete_user_conversations(
        db: Session,
        user_id: int
    ):
        """
        Delete all conversations of a user.
        """

        try:

            deleted_count = (
                db.query(Conversation)
                .filter(Conversation.user_id == user_id)
                .delete()
            )

            db.commit()

            logger.info(
                f"✅ Deleted {deleted_count} "
                f"conversations for user_id={user_id}"
            )

            return True

        except SQLAlchemyError as e:

            db.rollback()

            logger.error(
                f"❌ Failed to delete conversations: "
                f"{str(e)}"
            )

            return False
conversation_service=ConversationService()