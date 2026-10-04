from app.database.db import SessionLocal

from app.services.conversation_service import (
    ConversationService
)


db = SessionLocal()


# Save message
ConversationService.save_message(
    db=db,
    user_id=1,
    role="user",
    message="Hello AI"
)


# Fetch memory
conversations = (
    ConversationService.get_recent_conversations(
        db=db,
        user_id=1
    )
)


# Build AI memory
memory = (
    ConversationService.build_chat_memory(
        conversations
    )
)

print(memory)