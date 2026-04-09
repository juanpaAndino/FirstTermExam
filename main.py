from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel
from typing import Optional

app = FastAPI()

class User(SQLModel):
    id: Optional[int] = None
    username: str
    password: str
    email: Optional[str] = None
    is_active: bool = True

db_users = [
    User(id=1, username="admin", password="api", email="admin@u.edu.ec", is_active=True),
    User(id=2, username="user", password="user", email="user@u.edu.ec", is_active=True),
    User(id=3, username="guest", password="guest", email="guest@u.edu.ec", is_active=True)
]

@app.get("/")
def read_root():
    return {"Hello": "world"}

@app.post("/users")
def create_user(user: User):
    for u in db_users:
        if u.username == user.username or u.id == user.id:
            raise HTTPException(status_code=400, detail="El usuario o ID ya existe")
    
    if user.id is None:
        user.id = len(db_users) + 1
        
    db_users.append(user)
    return user

@app.get("/users")
def get_users():
    return db_users

@app.get("/users/{user_id}")
def get_user(user_id: int):
    for u in db_users:
        if u.id == user_id:
            return u
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.put("/users/{user_id}")
def update_user(user_id: int, user_data: User):
    for i, u in enumerate(db_users):
        if u.id == user_id:
            db_users[i].username = user_data.username
            db_users[i].email = user_data.email
            db_users[i].is_active = user_data.is_active
            return db_users[i]
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for i, u in enumerate(db_users):
        if u.id == user_id:
            db_users.pop(i)
            return {"message": "Usuario eliminado exitosamente"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.post("/login")
def login(user_login: User):
    for u in db_users:
        if u.username == user_login.username and u.password == user_login.password:
            return {"status": "success", "message": f"Bienvenido {u.username}"}
    
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")