from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from jwt_config import solicita_token
from fastapi.responses import JSONResponse
from validations import get_current_user
import schemas.users
import models.user
import crud.users
import config.db

user = APIRouter()

models.user.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user.get("/user/", response_model=List[schemas.users.user], tags=["Users"])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_users = crud.users.get_users(db=db, skip=skip, limit=limit)
    return db_users

@user.post("/user/", response_model=schemas.users.user, tags=["Usuarios"])
async def create_user(user_data: schemas.users.userCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_user = crud.users.create_user(db=db, user=user_data)
    return db_user

@user.put("/user/{id}", response_model=schemas.users.user, tags=["Usuarios"])
async def update_user(id: int, user_data: schemas.users.userUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_user = crud.users.update_user(db=db, user_id=id, user=user_data)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@user.delete("/user/{id}", response_model=schemas.users.user, tags=["Usuarios"])
async def delete_user(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_user = crud.users.delete_user(db=db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@user.post("/login/", response_model=schemas.users.user_login, tags=["User login"])
def read_credentials(user: schemas.users.user_login, db: Session = Depends(get_db)):
    db_credentials = crud.users.get_user_by_credentials(db, user_name = user.user_name, email = user.email, phone_number = user.phone_number, password = user.password)
    if db_credentials is None:
        return JSONResponse(content = {"Message": "Access denied"}, status_code=404)
    token: str = solicita_token(user.dict())
    return JSONResponse(status_code=200, content = token)
