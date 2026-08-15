from app.core.database import engine, Base
from app.users import models

print("Dropping old database tables...")
Base.metadata.drop_all(bind=engine)

print("Creating new database tables with updated schema...")
Base.metadata.create_all(bind=engine)

print("Database reset successfully! 🎉")
