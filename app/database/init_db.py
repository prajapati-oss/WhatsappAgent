from app.database.db import init_db
from app.database.session import engine
from app.database.models import Base

print("🚀 Creating database tables...")

Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully")

init_db()