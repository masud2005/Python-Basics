# FastAPI & PostgreSQL Setup Guide

This project is a professional basic setup for a FastAPI server (including PostgreSQL and Docker).

## Step 1: Create Project Folder and Environment

First, create a folder for the project and initialize a virtual environment inside it.

```bash
mkdir my-fastapi-app
cd my-fastapi-app
python -m venv venv
```

**Activate the environment:**
*   Windows: `source venv/Scripts/activate`
*   Mac/Linux: `source venv/bin/activate`

## Step 2: Install Packages

Install the necessary packages for the project:
```bash
pip install "fastapi[standard]" sqlalchemy psycopg2-binary pydantic-settings
```

## Step 3: Database Setup using Docker

Create a `docker-compose.yml` file in the root of the project:

```yaml
version: '3.8'

services:
  postgres_db:
    image: postgres:15
    container_name: fastapi_postgres
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: rootpassword
      POSTGRES_DB: fastapi_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Start the database by running the following command in the terminal:
```bash
docker compose up -d
```

## Step 4: Configuration and Security (`.env` and `config.py`)

Create a `.env` file in the root of the project:
```env
DATABASE_URL="postgresql://postgres:rootpassword@localhost:5432/fastapi_db"
```

Now, create a `config.py` file to read the data from the `.env` file:
```python
from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    DATABASE_URL : str
    
    class Config:
        env_file = ".env"

settings = Setting()
```

## Step 5: Database Connection (`database.py`)

Create `database.py` to connect to the database using SQLAlchemy:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Step 6: Create Database Models (`models.py`)

Create `models.py` to define the structure of your database tables:

```python
from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    age = Column(Integer)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
```

## Step 7: Main Application (`main.py`)

Finally, create the `main.py` file to connect everything and add logic to check the connection:

```python
from fastapi import FastAPI
from database import engine
import models

# Generate the tables in the database
models.Base.metadata.create_all(bind=engine)

# Check connection
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
```

## Step 8: Run the Server

After completing all the steps, start the server in the terminal:
```bash
uvicorn main:app --reload
```
