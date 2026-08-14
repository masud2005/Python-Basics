# pyrefly: ignore [missing-import]
from fastapi import FastAPI
from database import engine
import models

models.Base.metadata.create_all(bind=engine)

try:
    conn = engine.connect()
    print("✅ Database Connection Successful!")
    conn.close()
except Exception as e:
    print("❌ Error connecting to database:", e)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Server is Running..."}