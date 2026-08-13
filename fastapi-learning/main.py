
# pyrefly: ignore [missing-import]
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello FastAPI! I am ready."}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}, Welcome to FastAPI!"}

