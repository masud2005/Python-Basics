from fastapi import FastAPI
from app.core.database import engine
from app.users import models
from app.users.router import router as users_router

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Modular App",
    description="A professional, modular FastAPI backend.",
    version="1.0.0"
)

# Check database connection on startup
@app.on_event("startup")
def startup_event():
    try:
        conn = engine.connect()
        print("✅ Database Connection Successful!")
        conn.close()
    except Exception as e:
        print("❌ Error connecting to database:", e)


@app.get("/")
def read_root():
    return {"message": "Modular FastAPI Server is Running!"}

from app.auth.router import router as auth_router

# Include Routers
app.include_router(auth_router)
app.include_router(users_router)