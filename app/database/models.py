from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Boolean,
    Index
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.db import Base

from sqlalchemy.orm import declarative_base
# =========================================================
# USER MODEL
# =========================================================
Base = declarative_base()

class User(Base):

    __tablename__ = "users"

    # =====================================================
    # COLUMNS
    # =====================================================

    id = Column(Integer, primary_key=True, index=True)

    phone_number = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True
    )

    name = Column(String(255), nullable=True)

    language = Column(
        String(50),
        default="en"
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    conversations = relationship(
        "Conversation",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # =====================================================
    # INDEXES
    # =====================================================

    __table_args__ = (
        Index("idx_user_phone", "phone_number"),
    )

    # =====================================================
    # STRING REPRESENTATION
    # =====================================================

    def __repr__(self):
        return f"<User(id={self.id}, phone={self.phone_number})>"


# =========================================================
# CONVERSATION MODEL
# =========================================================

class Conversation(Base):

    __tablename__ = "conversations"

    # =====================================================
    # COLUMNS
    # =====================================================

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    role = Column(
        String(50),
        nullable=False
    )
    # Example:
    # user
    # assistant
    # system

    message = Column(
        Text,
        nullable=False
    )

    message_type = Column(
        String(50),
        default="text"
    )
    # text / image / audio / document

    whatsapp_message_id = Column(
        String(255),
        nullable=True
    )

    sentiment = Column(
        String(50),
        nullable=True
    )
    # positive / neutral / negative

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True
    )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    user = relationship(
        "User",
        back_populates="conversations"
    )

    # =====================================================
    # INDEXES
    # =====================================================

    __table_args__ = (

        Index(
            "idx_conversation_user_time",
            "user_id",
            "created_at"
        ),

        Index(
            "idx_conversation_role",
            "role"
        ),
    )

    # =====================================================
    # STRING REPRESENTATION
    # =====================================================

    def __repr__(self):
        return (
            f"<Conversation(id={self.id}, "
            f"user_id={self.user_id}, "
            f"role={self.role})>"
        )