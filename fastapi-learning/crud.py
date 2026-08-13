
# pyrefly: ignore [missing-import]
from fastapi import FastAPI, HTTPException
# pyrefly: ignore [missing-import]
from pydantic import BaseModel

app = FastAPI()

fake_db = {
    1: {"name": "Masud", "email": "masud@example.com"},
    2: {"name": "Rahim", "email": "rahim@example.com"}
}

# Define the User model for validation
class User(BaseModel):
    name: str
    email: str

# Read all users
@app.get("/users")
def get_all_users():
    return {
        "message": "All users retrieved successfully.",
        "data": fake_db
    }

# Read a single user by ID
@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found!")
    return {
        "message": "User retrieved successfully.",
        "data": fake_db[user_id]
    }

# Create a new user
@app.post("/create-user")
def create_user(user: User):
    # Generate the next ID (simple increment for this example)
    new_id = max(fake_db.keys()) + 1
    
    # Add the new user to the dictionary
    fake_db[new_id] = user.dict()
    
    return {
        "message": "User created successfully!",
        "data": fake_db[new_id]
    }

# Update an existing user
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found!")
    
    # Update the user's data
    fake_db[user_id] = user.dict()
    
    return {
        "message": "User updated successfully!",
        "data": fake_db[user_id]
    }

# Delete a user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found!")
    
    # Remove the user
    del fake_db[user_id]
    
    return {
        "message": "User deleted successfully!"
    }