from app.database.db import SessionLocal
from app.services.user_services import UserService


db = SessionLocal()

user = UserService.get_or_create_user(
    db=db,
    phone_number="916389627495",
    name="Rakesh"
)

print(user)