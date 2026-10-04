import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database.models import User


# =========================================================
# LOGGING CONFIG
# =========================================================

logger = logging.getLogger(__name__)


# =========================================================
# USER SERVICE
# =========================================================

class UserService:


    # =====================================================
    # GET USER BY PHONE NUMBER
    # =====================================================

    @staticmethod
    def get_user_by_phone(
        db: Session,
        phone_number: str
    ):
        """
        Fetch user using phone number.
        """

        try:

            user = (
                db.query(User)
                .filter(User.phone_number == phone_number)
                .first()
            )

            return user

        except SQLAlchemyError as e:

            logger.error(
                f"❌ Failed to fetch user: {str(e)}"
            )

            return None


    # =====================================================
    # CREATE NEW USER
    # =====================================================

    @staticmethod
    def create_user(
        db: Session,
        phone_number: str,
        name: str = None
    ):
        """
        Create new WhatsApp user.
        """

        try:

            new_user = User(
                phone_number=phone_number,
                name=name
            )

            db.add(new_user)

            db.commit()

            db.refresh(new_user)

            logger.info(
                f"✅ New user created: {phone_number}"
            )

            return new_user

        except SQLAlchemyError as e:

            db.rollback()

            logger.error(
                f"❌ Failed to create user: {str(e)}"
            )

            return None


    # =====================================================
    # GET OR CREATE USER
    # =====================================================

    @staticmethod
    def get_or_create_user(
        db: Session,
        phone_number: str,
        name: str = None
    ):
        """
        Fetch existing user.
        Create if not exists.
        """

        try:

            user = UserService.get_user_by_phone(
                db=db,
                phone_number=phone_number
            )

            if user:

                logger.info(
                    f"ℹ️ Existing user found: {phone_number}"
                )

                return user

            logger.info(
                f"ℹ️ Creating new user: {phone_number}"
            )

            return UserService.create_user(
                db=db,
                phone_number=phone_number,
                name=name
            )

        except Exception as e:

            logger.error(
                f"❌ get_or_create_user failed: {str(e)}"
            )

            return None


    # =====================================================
    # UPDATE USER NAME
    # =====================================================

    @staticmethod
    def update_user_name(
        db: Session,
        user_id: int,
        new_name: str
    ):
        """
        Update user name.
        """

        try:

            user = (
                db.query(User)
                .filter(User.id == user_id)
                .first()
            )

            if not user:

                logger.warning(
                    f"⚠️ User not found: {user_id}"
                )

                return None

            user.name = new_name

            db.commit()

            db.refresh(user)

            logger.info(
                f"✅ User updated: {user_id}"
            )

            return user

        except SQLAlchemyError as e:

            db.rollback()

            logger.error(
                f"❌ Failed to update user: {str(e)}"
            )

            return None

user_service=UserService()